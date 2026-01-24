"""
Email configuration for contact form notifications.
Uses Resend API for reliable email delivery on cloud platforms.
Falls back to SMTP if Resend is not configured.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables before accessing them
load_dotenv()

# Check which email provider to use
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
USE_RESEND = bool(RESEND_API_KEY)

if USE_RESEND:
    import resend
    resend.api_key = RESEND_API_KEY
    print("📧 Using Resend API for email delivery")
else:
    from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
    
    # SMTP configuration (fallback)
    mail_port = int(os.getenv("MAIL_PORT", "465"))
    use_ssl = mail_port == 465
    
    conf = ConnectionConfig(
        MAIL_USERNAME=os.getenv("MAIL_USERNAME", ""),
        MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", ""),
        MAIL_FROM=os.getenv("MAIL_FROM", "noreply@example.com"),
        MAIL_PORT=mail_port,
        MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
        MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME", "Portfolio Contact"),
        MAIL_STARTTLS=not use_ssl,
        MAIL_SSL_TLS=use_ssl,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
        TEMPLATE_FOLDER=Path(__file__).parent / "templates",
    )
    fm = FastMail(conf)
    print("📧 Using SMTP for email delivery")


def is_email_configured() -> bool:
    """Check if email credentials are configured"""
    if USE_RESEND:
        return bool(RESEND_API_KEY)
    return bool(os.getenv("MAIL_USERNAME") and os.getenv("MAIL_PASSWORD"))


async def send_contact_notification(
    name: str,
    email: str,
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

    sender_email = os.getenv("MAIL_FROM", "onboarding@resend.dev")
    sender_name = os.getenv("MAIL_FROM_NAME", "Portfolio Contact")

    # Build HTML content
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2 style="color: #6366f1;">New Contact Form Submission</h2>
        <div style="background: #f3f4f6; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> <a href="mailto:{email}">{email}</a></p>
            <p><strong>Message:</strong></p>
            <p style="background: white; padding: 15px; border-radius: 4px;">{message}</p>
        </div>
        <p style="color: #6b7280; font-size: 12px;">Sent from IP: {ip_address}</p>
    </body>
    </html>
    """

    try:
        if USE_RESEND:
            # Use Resend API
            params = {
                "from": f"{sender_name} <{sender_email}>",
                "to": [recipient],
                "subject": f"Portfolio Contact: {name}",
                "html": html_content,
                "reply_to": email,
            }
            result = resend.Emails.send(params)
            print(f"✓ Email sent via Resend. ID: {result.get('id', 'unknown')}")
            return True
        else:
            # Use SMTP (fastapi-mail)
            message_schema = MessageSchema(
                subject=f"Portfolio Contact: {name}",
                recipients=[recipient],
                body=html_content,
                subtype=MessageType.html,
            )
            await fm.send_message(message_schema)
            print(f"✓ Email notification sent via SMTP for message from {email}")
            return True
            
    except Exception as e:
        print(f"✗ Failed to send email: {e}")
        return False
