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

    # Build HTML content - Professional design matching original template
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>New Portfolio Message</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background-color: #f5f5f5;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <!-- Header with gradient -->
            <tr>
                <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center;">
                    <h1 style="margin: 0; color: #ffffff; font-size: 24px; font-weight: 600;">
                        📬 New Portfolio Message
                    </h1>
                </td>
            </tr>
            
            <!-- Content -->
            <tr>
                <td style="padding: 30px;">
                    <!-- From -->
                    <div style="margin-bottom: 20px;">
                        <label style="display: block; color: #6366f1; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">FROM</label>
                        <div style="background-color: #f9fafb; padding: 12px 16px; border-radius: 8px; border: 1px solid #e5e7eb;">
                            {name}
                        </div>
                    </div>
                    
                    <!-- Email -->
                    <div style="margin-bottom: 20px;">
                        <label style="display: block; color: #6366f1; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">EMAIL</label>
                        <div style="background-color: #f9fafb; padding: 12px 16px; border-radius: 8px; border: 1px solid #e5e7eb;">
                            <a href="mailto:{email}" style="color: #3b82f6; text-decoration: none;">{email}</a>
                        </div>
                    </div>
                    
                    <!-- Message -->
                    <div style="margin-bottom: 20px;">
                        <label style="display: block; color: #6366f1; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">MESSAGE</label>
                        <div style="background-color: #f9fafb; padding: 16px; border-radius: 8px; border-left: 4px solid #a3e635; border-top: 1px solid #e5e7eb; border-right: 1px solid #e5e7eb; border-bottom: 1px solid #e5e7eb;">
                            <p style="margin: 0; white-space: pre-wrap; line-height: 1.6;">{message}</p>
                        </div>
                    </div>
                    
                    <!-- IP Address -->
                    <div style="background-color: #fef9c3; padding: 12px 16px; border-radius: 8px; margin-top: 20px;">
                        <span style="color: #ca8a04;">🌐 Sender IP: {ip_address}</span>
                    </div>
                </td>
            </tr>
            
            <!-- Footer -->
            <tr>
                <td style="padding: 20px 30px; text-align: center; border-top: 1px solid #e5e7eb;">
                    <p style="margin: 0; color: #9ca3af; font-size: 13px;">
                        Sent from your Portfolio Contact Form
                    </p>
                </td>
            </tr>
        </table>
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
