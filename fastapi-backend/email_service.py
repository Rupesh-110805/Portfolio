"""
Email configuration for contact form notifications.
Uses fastapi-mail for async email sending.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables before accessing them
load_dotenv()

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr

# Email configuration from environment variables
# Note: Use port 465 with SSL for cloud platforms that block port 587
mail_port = int(os.getenv("MAIL_PORT", "465"))
use_ssl = mail_port == 465  # Use SSL for port 465, STARTTLS for 587

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", ""),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", ""),
    MAIL_FROM=os.getenv("MAIL_FROM", "noreply@example.com"),
    MAIL_PORT=mail_port,
    MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME", "Portfolio Contact"),
    MAIL_STARTTLS=not use_ssl,  # Use STARTTLS only for port 587
    MAIL_SSL_TLS=use_ssl,  # Use SSL for port 465
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / "templates",
)

# FastMail instance
fm = FastMail(conf)


def is_email_configured() -> bool:
    """Check if email credentials are configured"""
    return bool(os.getenv("MAIL_USERNAME") and os.getenv("MAIL_PASSWORD"))


async def send_contact_notification(
    name: str,
    email: EmailStr,
    message: str,
    ip_address: str,
) -> bool:
    """
    Send email notification for new contact form submission.
    Returns True if sent successfully, False otherwise.
    """
    if not is_email_configured():
        print("⚠️  Email not configured. Skipping notification.")
        return False

    recipient = os.getenv("MAIL_TO", os.getenv("MAIL_FROM", ""))
    if not recipient:
        print("⚠️  No recipient email configured.")
        return False

    try:
        message_schema = MessageSchema(
            subject=f"Portfolio Contact: {name}",
            recipients=[recipient],
            template_body={
                "name": name,
                "email": email,
                "message": message,
                "ip_address": ip_address,
            },
            subtype=MessageType.html,
        )
        await fm.send_message(message_schema, template_name="email.html")
        print(f"✓ Email notification sent for message from {email}")
        return True
    except Exception as e:
        print(f"✗ Failed to send email: {e}")
        return False
