from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class BlogImageRead(BaseModel):
    id: int
    blog_id: int
    link_to_disk: str
    public_url: str
    is_preview: bool
    uploaded_at: datetime

    class Config:
        from_attributes = True


class BlogImageUpdate(BaseModel):
    caption: Optional[str] = None
    ordering: Optional[int] = None


class BlogBase(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    is_published: bool = False


class BlogCreate(BlogBase):
    pass


class BlogRead(BlogBase):
    id: int
    created_at: datetime
    updated_at: datetime
    images: List[BlogImageRead] = []

    class Config:
        from_attributes = True


class BlogUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    is_published: Optional[bool] = None
