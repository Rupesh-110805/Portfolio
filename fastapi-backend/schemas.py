from pydantic import BaseModel, EmailStr
from typing import Optional


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
    email: str
    message: str


class MessageCreate(MessageBase):
    pass


class MessageResponse(MessageBase):
    id: int

    class Config:
        from_attributes = True
