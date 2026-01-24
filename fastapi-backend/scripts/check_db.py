"""
Database check script - verifies SQLite table structure and integrity.
"""
import sqlite3
import os
from pathlib import Path

# Navigate to backend directory
backend_dir = Path(__file__).parent.parent
db_path = backend_dir / "portfolio.db"

print(f"📂 Checking database at: {db_path}")
print("-" * 50)

if not db_path.exists():
    print("❌ Database file not found!")
    print("   Run the FastAPI server once to create it, or run seed.py")
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
    
    print("-" * 50)
    
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
            print(f"❌ Missing table: {table_name}")
        else:
            # Show columns for each table
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            print(f"✓ Table '{table_name}' columns:")
            for col in columns:
                print(f"    - {col[1]} ({col[2]})")
            
            # Count records
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"    → {count} records")
    
    print("-" * 50)
    
    if missing_tables:
        print(f"❌ Missing tables: {', '.join(missing_tables)}")
        print("   Recommendation: Delete portfolio.db and restart the FastAPI server")
    else:
        print("✓ All required tables exist!")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Error checking database: {e}")
    exit(1)
