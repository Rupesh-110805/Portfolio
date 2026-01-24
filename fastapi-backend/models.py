from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    tech_stack = Column(JSON, nullable=False)  # JSON for SQLite compatibility
    link = Column(String, nullable=True)
    github_link = Column(String, nullable=True)
    image_url = Column(String, nullable=False)


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)  # 'Languages', 'Frameworks', 'Tools'


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    message = Column(String, nullable=False)
    ip_address = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class BlockedSender(Base):
    """Store blocked emails and IPs for shadowbanning spammers"""
    __tablename__ = "blocked_senders"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=True, index=True)
    ip_address = Column(String, nullable=True, index=True)
    reason = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
