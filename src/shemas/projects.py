import uuid

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ImageRead(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    path_to_file: str
    public_url: str
    is_preview: bool
    is_plan: bool
    is_gallery: bool
    uploaded_at: datetime

    class Config:
        from_attributes = True


class ImageUpdate(BaseModel):
    caption: Optional[str] = None
    ordering: Optional[int] = None


class StorageProject(BaseModel):
    slug: str
    content_type: str


class ProjectBase(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    is_published: bool = False


class ProjectCreate(ProjectBase):
    shot_description: str
    quadrature: int
    floors: int = 1
    bedrooms: int = 1


class ImageCreate(BaseModel):
    path_to_file: str
    public_url: str


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    is_published: Optional[bool] = None
    shot_description: str
    quadrature: int
    floors: int = 1
    bedrooms: int = 1


class ProjectRead(ProjectBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    images: List[ImageRead] = []
    shot_description: str
    quadrature: int
    floors: int
    bedrooms: int

    class Config:
        from_attributes = True


class TelegramAuthData(BaseModel):
    id: uuid.UUID
    first_name: str
    username: Optional[str] = None
    photo_url: Optional[str] = None
    auth_date: int
    hash: str


class PassLoginRequest(BaseModel):
    login: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    is_admin: bool
