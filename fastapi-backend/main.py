from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from database import engine, get_db, Base
from models import Project, Skill, Message
from schemas import (
    ProjectCreate, ProjectResponse,
    SkillResponse,
    MessageCreate, MessageResponse,
)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Dev Portfolio API",
    description="FastAPI backend for the developer portfolio",
    version="1.0.0",
)

# CORS middleware - allow Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


# ==================== MESSAGES ====================

@app.post("/api/messages", response_model=MessageResponse, status_code=201)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    """Create a new contact message"""
    db_message = Message(
        name=message.name,
        email=message.email,
        message=message.message,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


# ==================== HEALTH CHECK ====================

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
