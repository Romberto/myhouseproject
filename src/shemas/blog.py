import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from src.core.models.blog import BlogCategory


class BlogImageRead(BaseModel):
    id: uuid.UUID
    blog_id: uuid.UUID
    path_to_file: str
    public_url: str
    is_preview: bool
    shot_description: str
    uploaded_at: datetime

    class Config:
        from_attributes = True


class BlogImageUpdate(BaseModel):
    caption: Optional[str] = None
    ordering: Optional[int] = None


class BlogBase(BaseModel):
    title: str
    slug: str
    category: Optional[str] = None
    category: BlogCategory



class BlogCreate(BlogBase):
    article: str
    excerpt: str

class BlogRead(BlogBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    article: str
    excerpt: str
    path_to_file: Optional[str] = None
    public_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class BlogUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    is_published: Optional[bool] = None
    shot_description: Optional[str] = None



