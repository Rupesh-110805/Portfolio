"""
FastAPI backend for the developer portfolio.
Features: Rate limiting, honeypot spam protection, shadowbanning, async email notifications.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI, Depends, HTTPException, Request, Header, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from database import engine, get_db, Base
from models import Project, Skill, Message, BlockedSender
from schemas import (
    ProjectCreate, ProjectResponse,
    SkillResponse,
    MessageCreate, MessageResponse,
    BlockSenderRequest, BlockedSenderResponse,
)
from email_service import send_contact_notification, is_email_configured

# Create tables
Base.metadata.create_all(bind=engine)

# Rate limiter setup
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Dev Portfolio API",
    description="FastAPI backend for the developer portfolio",
    version="1.0.0",
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware - allow Next.js frontend
# Build origins list, filtering out empty strings
cors_origins = [
    "http://localhost:3000",  # Next.js dev server
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
# Add production frontend URL if configured
frontend_url = os.getenv("FRONTEND_URL", "")
if frontend_url:
    cors_origins.append(frontend_url)
    # Also allow without trailing slash
    cors_origins.append(frontend_url.rstrip("/"))

print(f"📋 CORS allowed origins: {cors_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Admin secret for protected routes
ADMIN_SECRET = os.getenv("ADMIN_SECRET", "change-me-in-production")


# ==================== HELPER FUNCTIONS ====================

def get_client_ip(request: Request) -> str:
    """Get the real client IP, considering proxies"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def is_sender_blocked(db: Session, email: str, ip_address: str) -> bool:
    """
    Check if the sender is shadowbanned.
    Returns True if blocked (should skip email but return success).
    """
    blocked = db.query(BlockedSender).filter(
        (BlockedSender.email == email) | (BlockedSender.ip_address == ip_address)
    ).first()
    return blocked is not None


# ==================== PROJECTS ====================

@app.get("/api/projects", response_model=List[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    """Get all projects"""
    projects = db.query(Project).all()
    return projects


@app.post("/api/projects", response_model=ProjectResponse, status_code=201)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project"""
    db_project = Project(
        title=project.title,
        description=project.description,
        tech_stack=project.tech_stack,
        link=project.link,
        github_link=project.github_link,
        image_url=project.image_url,
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


# ==================== SKILLS ====================

@app.get("/api/skills", response_model=List[SkillResponse])
def get_skills(db: Session = Depends(get_db)):
    """Get all skills"""
    skills = db.query(Skill).all()
    return skills


# ==================== MESSAGES (Contact Form) ====================

@app.post("/api/messages", response_model=MessageResponse, status_code=201)
@limiter.limit("100/hour")  # Rate limit: 100 messages per hour per IP (for testing, change to 3/hour in production)
async def create_message(
    request: Request,
    message: MessageCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Create a new contact message with spam protection.
    
    Features:
    - Rate limiting (3/hour per IP)
    - Honeypot field (bot_check)
    - Shadowbanning (blocked senders get fake success)
    - Async email notification
    """
    ip_address = get_client_ip(request)
    
    # 1. Honeypot check - if bot_check has value, it's a bot
    if message.bot_check:
        print(f"🤖 Bot detected (honeypot triggered) from IP: {ip_address}")
        # Return fake success to confuse the bot
        return MessageResponse(
            id=0,
            name=message.name,
            email=message.email,
            message=message.message,
            created_at=None,
        )
    
    # 2. Shadowban check - if blocked, skip email but return success
    if is_sender_blocked(db, message.email, ip_address):
        print(f"🚫 Shadowbanned sender: {message.email} / {ip_address}")
        # Store message but don't send email
        db_message = Message(
            name=message.name,
            email=message.email,
            message=message.message,
            ip_address=ip_address,
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message
    
    # 3. Legitimate message - save and send email
    db_message = Message(
        name=message.name,
        email=message.email,
        message=message.message,
        ip_address=ip_address,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # 4. Send email notification in background (non-blocking)
    print(f"📧 Checking email config: is_email_configured={is_email_configured()}")
    if is_email_configured():
        async def send_email_with_logging():
            try:
                print(f"📤 Attempting to send email notification to owner...")
                result = await send_contact_notification(
                    name=message.name,
                    email=message.email,
                    message=message.message,
                    ip_address=ip_address,
                )
                print(f"📧 Email send result: {result}")
            except Exception as e:
                print(f"❌ Email background task error: {e}")
                import traceback
                traceback.print_exc()
        
        background_tasks.add_task(send_email_with_logging)
    else:
        print("⚠️ Email not configured, skipping notification")
    
    return db_message


# ==================== ADMIN ROUTES ====================

def verify_admin_secret(x_admin_secret: Optional[str] = Header(None)) -> bool:
    """Verify admin secret header"""
    if not x_admin_secret or x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Invalid admin secret")
    return True


@app.post("/api/admin/block", response_model=BlockedSenderResponse, status_code=201)
def block_sender(
    block_request: BlockSenderRequest,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin_secret),
):
    """
    Block a sender by email and/or IP address.
    Requires X-Admin-Secret header.
    """
    if not block_request.email and not block_request.ip_address:
        raise HTTPException(
            status_code=400,
            detail="Must provide at least email or ip_address"
        )
    
    # Check if already blocked
    existing = db.query(BlockedSender).filter(
        (BlockedSender.email == block_request.email) |
        (BlockedSender.ip_address == block_request.ip_address)
    ).first()
    
    if existing:
        raise HTTPException(status_code=409, detail="Sender already blocked")
    
    blocked = BlockedSender(
        email=block_request.email,
        ip_address=block_request.ip_address,
        reason=block_request.reason,
    )
    db.add(blocked)
    db.commit()
    db.refresh(blocked)
    
    print(f"🚫 Blocked sender: {block_request.email or block_request.ip_address}")
    return blocked


@app.get("/api/admin/blocked", response_model=List[BlockedSenderResponse])
def list_blocked_senders(
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin_secret),
):
    """List all blocked senders. Requires X-Admin-Secret header."""
    return db.query(BlockedSender).all()


@app.delete("/api/admin/block/{block_id}", status_code=204)
def unblock_sender(
    block_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin_secret),
):
    """Remove a sender from the blocklist. Requires X-Admin-Secret header."""
    blocked = db.query(BlockedSender).filter(BlockedSender.id == block_id).first()
    if not blocked:
        raise HTTPException(status_code=404, detail="Blocked sender not found")
    
    db.delete(blocked)
    db.commit()
    return None


@app.get("/api/admin/messages", response_model=List[MessageResponse])
def list_messages(
    db: Session = Depends(get_db),
    _: bool = Depends(verify_admin_secret),
):
    """List all contact messages. Requires X-Admin-Secret header."""
    return db.query(Message).order_by(Message.created_at.desc()).all()


# ==================== HEALTH CHECK ====================

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "email_configured": is_email_configured(),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
