from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ImageRead(BaseModel):
    id: int
    project_id: int
    file_path: str
    caption: Optional[str] = None
    ordering: int
    uploaded_at: datetime

    class Config:
        from_attributes = True


class ImageUpdate(BaseModel):
    caption: Optional[str] = None
    ordering: Optional[int] = None


class ProjectBase(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    is_published: bool = False


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    is_published: Optional[bool] = None
    preview_image_id: Optional[int] = None


class ProjectRead(ProjectBase):
    id: int
    preview_image_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    # images: List[ImageRead] = []

    class Config:
        from_attributes = True


class TelegramAuthData(BaseModel):
    id: int
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
