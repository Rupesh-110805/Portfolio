"""
Seed script to populate the database with initial data.
Run with: python seed.py
"""
from database import SessionLocal, engine, Base
from models import Project, Skill

# Create tables
Base.metadata.create_all(bind=engine)


def seed_database():
    db = SessionLocal()

    try:
        # Check if projects already exist
        existing_projects = db.query(Project).count()
        if existing_projects == 0:
            projects = [
                Project(
                    title="CSES-solutions",
                    description="A curated collection of solutions to problems on the CSES Problem Set. Solutions are written in modern C++, focused on competitive programming techniques like dynamic programming, graphs, and greedy algorithms.",
                    tech_stack=["C++", "Algorithms", "DSA"],
                    github_link="https://github.com/Rupesh-110805/CSES-solutions",
                    image_url="https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&q=80&w=1000",
                ),
                Project(
                    title="DDoS Attack Detection",
                    description="A machine learning-based DDoS attack detection system using network traffic analysis. Implements classification models to identify malicious traffic patterns in real-time.",
                    tech_stack=["FastAPI", "Network Security"],
                    github_link="https://github.com/Rupesh-110805/DDoS-Attack-Detection",
                    image_url="/ddos-project.png",
                ),
                Project(
                    title="django-chat-app",
                    description="A real-time chat application built with Django and WebSockets. Users can exchange messages in chat rooms with session management and intuitive UI.",
                    tech_stack=["Django", "WebSockets", "PostgreSQL", "Redis"],
                    github_link="https://github.com/Rupesh-110805/django-chat-app",
                    image_url="/django-chat-app.png",
                ),
                Project(
                    title="Pneumonia-Detection-XAI",
                    description="A pneumonia detection model using CNN with explainable AI (XAI) visualizations on chest X-rays. Provides interpretability for medical imaging decisions.",
                    tech_stack=["Python", "PyTorch", "Deep Learning", "XAI"],
                    github_link="https://github.com/Rupesh-110805/Pneumonia-Detection-XAI",
                    image_url="https://images.unsplash.com/photo-1530213786676-41ad9f7736f6?auto=format&fit=crop&q=80&w=1000",
                ),
                Project(
                    title="Talent-flow",
                    description="A mini hiring platform built with TypeScript and modern frontend stack. Includes project-level features like search, filters, and intuitive UI components.",
                    tech_stack=["TypeScript", "React", "Frontend Design"],
                    github_link="https://github.com/Rupesh-110805/Talent-flow",
                    image_url="https://images.unsplash.com/photo-1586281380349-632531db7ed4?auto=format&fit=crop&q=80&w=1000",
                ),
            ]
            db.add_all(projects)
            print("✓ Seeded projects")

        # Check if skills already exist
        existing_skills = db.query(Skill).count()
        if existing_skills == 0:
            skills = [
                # Languages
                Skill(name="C++", category="Languages"),
                Skill(name="Python", category="Languages"),
                Skill(name="SQL", category="Languages"),
                Skill(name="JavaScript", category="Languages"),
                Skill(name="TypeScript", category="Languages"),
                # Frameworks
                Skill(name="React", category="Frameworks"),
                Skill(name="Django", category="Frameworks"),
                Skill(name="FastAPI", category="Frameworks"),
                Skill(name="Flask", category="Frameworks"),
                Skill(name="Machine Learning", category="Frameworks"),
                Skill(name="CNNs", category="Frameworks"),
                # Tools
                Skill(name="Linux", category="Tools"),
                Skill(name="Docker", category="Tools"),
                Skill(name="Git/GitHub", category="Tools"),
                Skill(name="GitHub Actions", category="Tools"),
                Skill(name="WebSockets", category="Tools"),
                Skill(name="DSA", category="Tools"),
                Skill(name="Competitive Programming", category="Tools"),
            ]
            db.add_all(skills)
            print("✓ Seeded skills")

        db.commit()
        print("✓ Database seeding complete!")

    except Exception as e:
        print(f"✗ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
