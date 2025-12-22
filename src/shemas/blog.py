import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from src.core.models.blog import BlogCategory


class BlogBase(BaseModel):
    title: str
    slug: str
    category: Optional[str] = BlogCategory.tips
    path_to_file: Optional[str] = None
    public_url: Optional[str] = None
    is_published: Optional[bool] = None

class BlogCreate(BlogBase):
    article: Optional[str] = None
    excerpt: Optional[str] = None


class BlogRead(BlogBase):
    id: uuid.UUID
    article: Optional[str]
    excerpt: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class BlogUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    article: Optional[str] = None
    excerpt: Optional[str] = None





