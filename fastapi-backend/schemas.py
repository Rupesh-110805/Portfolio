from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# Project schemas
class ProjectBase(BaseModel):
    title: str
    description: str
    tech_stack: list[str]
    link: Optional[str] = None
    github_link: Optional[str] = None
    image_url: str


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int

    class Config:
        from_attributes = True


# Skill schemas
class SkillBase(BaseModel):
    name: str
    category: str


class SkillCreate(SkillBase):
    pass


class SkillResponse(SkillBase):
    id: int

    class Config:
        from_attributes = True


# Message schemas
class MessageBase(BaseModel):
    name: str
    email: EmailStr
    message: str


class MessageCreate(MessageBase):
    # Honeypot field - should always be empty from real users
    # Bots often fill in all fields, so if this has a value, it's a bot
    bot_check: Optional[str] = None


class MessageResponse(MessageBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# BlockedSender schemas
class BlockSenderRequest(BaseModel):
    email: Optional[str] = None
    ip_address: Optional[str] = None
    reason: Optional[str] = None


class BlockedSenderResponse(BaseModel):
    id: int
    email: Optional[str]
    ip_address: Optional[str]
    reason: Optional[str]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True
