---
description: Run backend diagnostics (Database and Email check)
---

# Backend Diagnostics

This workflow runs diagnostic scripts to verify the backend database structure and email configuration.

## 1. Check Database Structure

This step verifies that the SQLite database exists and has the required tables.

```python
# Create temporary check_db.py
import sqlite3
import os
from pathlib import Path

# Navigate to backend directory
backend_dir = Path("fastapi-backend").resolve()
db_path = backend_dir / "portfolio.db"

print(f"📂 Checking database at: {db_path}")
print("-" * 50)

if not db_path.exists():
    print("❌ Database file not found!")
    exit(1)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # List all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"✓ Found {len(tables)} tables:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # Check required tables
    required_tables = ["projects", "skills", "messages", "blocked_senders"]
    missing_tables = []
    
    for table_name in required_tables:
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?;", 
            (table_name,)
        )
        if not cursor.fetchone():
            missing_tables.append(table_name)
    
    if missing_tables:
        print(f"❌ Missing tables: {', '.join(missing_tables)}")
    else:
        print("✓ All required tables exist!")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Error checking database: {e}")
    exit(1)
```

## 2. Test Email Configuration

This step sends a test email using the configuration in `.env`.

**Prerequisites:**
- `fastapi-backend/.env` must be configured with SMTP details.

```python
# Create temporary test_email.py
import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

backend_dir = Path("fastapi-backend").resolve()
sys.path.insert(0, str(backend_dir))
load_dotenv(backend_dir / ".env")

async def test_email():
    try:
        from email_service import send_contact_notification, is_email_configured
        
        if not is_email_configured():
            print("❌ Email is not configured")
            return
            
        print("✓ Email credentials are configured")
        
        recipient = os.getenv("MAIL_TO", os.getenv("MAIL_FROM"))
        print(f"📤 Sending test email to: {recipient}")
        
        result = await send_contact_notification(
            name="Diagnostic Test",
            email="test@example.com",
            message="Diagnostic test message.",
            ip_address="127.0.0.1"
        )
        
        if result:
            print("✓ Email sent successfully!")
        else:
            print("❌ Email sending failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    if os.path.exists(str(backend_dir / "email_service.py")):
         asyncio.run(test_email())
    else:
         print("Skipping email test (email_service.py not found)")
```
