# Developer Portfolio

A modern, full-stack portfolio website showcasing my projects, skills, and contact information.

![Next.js](https://img.shields.io/badge/Next.js-14-black?style=flat-square&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=flat-square&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178C6?style=flat-square&logo=typescript&logoColor=white)

## 🚀 Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Modern UI components
- **Lucide Icons** - Beautiful icons

### Backend
- **FastAPI** - High-performance Python web framework
- **SQLAlchemy** - Python ORM
- **SQLite** (dev) / **PostgreSQL** (prod) - Database
- **Pydantic** - Data validation

## 📁 Project Structure

```
Dev-Portfolio/
├── fastapi-backend/       # Python FastAPI backend
│   ├── main.py            # API endpoints
│   ├── models.py          # Database models
│   ├── database.py        # DB connection
│   └── seed.py            # Initial data
├── nextjs-frontend/       # Next.js frontend
│   ├── src/
│   │   ├── app/           # App Router pages
│   │   ├── components/    # React components
│   │   ├── hooks/         # Custom hooks
│   │   └── lib/           # Utilities
│   └── public/            # Static assets
└── attached_assets/       # Project images
```

## 🛠️ Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd fastapi-backend
python -m venv venv
.\venv\Scripts\Activate      # Windows
# source venv/bin/activate   # Linux/Mac

pip install -r requirements.txt
python seed.py               # Seed database
uvicorn main:app --reload --port 8000
```

### Frontend Setup

```bash
cd nextjs-frontend
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the portfolio.

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects` | Get all projects |
| POST | `/api/projects` | Create a project |
| GET | `/api/skills` | Get all skills |
| POST | `/api/messages` | Send a message |
| GET | `/api/health` | Health check |

## 📂 Featured Projects

| Project | Description | Tech Stack |
|---------|-------------|------------|
| [CSES-solutions](https://github.com/Rupesh-110805/CSES-solutions) | Competitive programming solutions in C++ | C++, Algorithms, DSA |
| [DDoS Attack Detection](https://github.com/Rupesh-110805/DDoS-Attack-Detection) | ML-based network attack detection system | FastAPI, Network Security |
| [django-chat-app](https://github.com/Rupesh-110805/django-chat-app) | Real-time chat with Django & WebSockets | Django, WebSockets, PostgreSQL, Redis |
| [Pneumonia-Detection-XAI](https://github.com/Rupesh-110805/Pneumonia-Detection-XAI) | CNN with explainable AI for chest X-rays | Python, PyTorch, Deep Learning, XAI |
| [Talent-flow](https://github.com/Rupesh-110805/Talent-flow) | Mini hiring platform with modern UI | TypeScript, React |

## 👤 Author

**Rupesh**
- GitHub: [@Rupesh-110805](https://github.com/Rupesh-110805)

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
