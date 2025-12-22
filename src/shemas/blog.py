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
    article: str
    excerpt: str


class BlogRead(BlogBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    article: str
    excerpt: str

    model_config = ConfigDict(from_attributes=True)


class BlogUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None





