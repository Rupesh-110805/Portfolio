"""
Email test script - verifies email configuration and sends a test email.
"""
import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / ".env")

print("=" * 50)
print("📧 EMAIL CONFIGURATION TEST")
print("=" * 50)

# Check environment variables
mail_vars = {
    "MAIL_SERVER": os.getenv("MAIL_SERVER"),
    "MAIL_PORT": os.getenv("MAIL_PORT"),
    "MAIL_USERNAME": os.getenv("MAIL_USERNAME"),
    "MAIL_PASSWORD": "***SET***" if os.getenv("MAIL_PASSWORD") else "❌ NOT SET",
    "MAIL_FROM": os.getenv("MAIL_FROM"),
    "MAIL_FROM_NAME": os.getenv("MAIL_FROM_NAME"),
    "MAIL_TO": os.getenv("MAIL_TO"),
}

print("\n📋 Environment Variables:")
for key, value in mail_vars.items():
    status = "✓" if value and value != "❌ NOT SET" else "❌"
    # Mask password
    display_value = value if key != "MAIL_PASSWORD" else value
    print(f"  {status} {key}: {display_value or '(not set)'}")

# Check for missing critical vars
critical_missing = []
if not os.getenv("MAIL_USERNAME"):
    critical_missing.append("MAIL_USERNAME")
if not os.getenv("MAIL_PASSWORD"):
    critical_missing.append("MAIL_PASSWORD")
if not os.getenv("MAIL_TO") and not os.getenv("MAIL_FROM"):
    critical_missing.append("MAIL_TO (or MAIL_FROM as fallback)")

if critical_missing:
    print(f"\n❌ CRITICAL: Missing required variables: {', '.join(critical_missing)}")
    print("   Email notifications will NOT work until these are set in .env")
    sys.exit(1)

print("\n" + "-" * 50)
print("🔄 Testing email sending...")

async def test_email():
    try:
        from email_service import send_contact_notification, is_email_configured
        
        if not is_email_configured():
            print("❌ Email is not configured (is_email_configured() returned False)")
            return False
        
        print("✓ Email credentials are configured")
        
        # Send test email
        recipient = os.getenv("MAIL_TO", os.getenv("MAIL_FROM"))
        print(f"📤 Sending test email to: {recipient}")
        
        result = await send_contact_notification(
            name="Test User",
            email="test@example.com",
            message="This is a test message from the portfolio contact form diagnostic script.\n\nIf you receive this, email is working correctly!",
            ip_address="127.0.0.1 (test)",
        )
        
        if result:
            print("✓ Email sent successfully!")
            print(f"  Check your inbox at: {recipient}")
            return True
        else:
            print("❌ Email sending failed (returned False)")
            return False
            
    except Exception as e:
        print(f"❌ Error during email test: {e}")
        import traceback
        traceback.print_exc()
        return False

# Run the async test
success = asyncio.run(test_email())

print("\n" + "=" * 50)
if success:
    print("✅ EMAIL TEST PASSED")
else:
    print("❌ EMAIL TEST FAILED")
    print("\nTroubleshooting tips:")
    print("  1. Verify MAIL_USERNAME and MAIL_PASSWORD in .env")
    print("  2. For Gmail, use an App Password (not your regular password)")
    print("     → Go to Google Account > Security > 2-Step Verification > App passwords")
    print("  3. Check if 'Less secure app access' needs to be enabled (not recommended)")
    print("  4. Ensure MAIL_SERVER and MAIL_PORT are correct (smtp.gmail.com:587 for Gmail)")
print("=" * 50)
