# Dev Portfolio - Next.js + FastAPI

This project has been migrated from Express/Vite to **Next.js** (frontend) + **FastAPI** (backend).

## Project Structure

```
Dev-Portfolio/
├── nextjs-frontend/     # Next.js 14 React frontend
│   ├── src/
│   │   ├── app/         # App Router pages
│   │   ├── components/  # React components
│   │   ├── hooks/       # React Query hooks
│   │   ├── lib/         # Utilities
│   │   └── types/       # TypeScript types
│   └── package.json
│
├── fastapi-backend/     # FastAPI Python backend
│   ├── main.py          # API routes
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── database.py      # DB connection
│   ├── seed.py          # Seed data script
│   └── requirements.txt
│
└── (original client/ and server/ folders preserved)
```

---

## Quick Start

### 1. Start FastAPI Backend

```powershell
cd fastapi-backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Set DATABASE_URL (PostgreSQL)
$env:DATABASE_URL="postgresql://user:password@localhost:5432/portfolio_db"

# Seed the database (optional, first run)
python seed.py

# Run the server
uvicorn main:app --reload --port 8000
```

Backend will be at: **http://localhost:8000**  
API docs at: **http://localhost:8000/docs**

---

### 2. Start Next.js Frontend

```powershell
cd nextjs-frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

Frontend will be at: **http://localhost:3000**

---

## API Endpoints

| Method | Endpoint         | Description           |
|--------|------------------|-----------------------|
| GET    | /api/projects    | List all projects     |
| POST   | /api/projects    | Create a project      |
| GET    | /api/skills      | List all skills       |
| POST   | /api/messages    | Submit contact form   |
| GET    | /api/health      | Health check          |

---

## Environment Variables

### FastAPI Backend
Create `.env` in `fastapi-backend/`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/portfolio_db
```

### Next.js Frontend
Create `.env.local` in `nextjs-frontend/`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Production Build

### FastAPI
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Next.js
```bash
npm run build
npm run start
```

---

## Notes

- The original `client/` and `server/` folders are preserved if you need to rollback.
- FastAPI uses SQLAlchemy with the same PostgreSQL database schema as the original Drizzle setup.
- CORS is configured to allow requests from `http://localhost:3000`.
