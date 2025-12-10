from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.core.models.base import Base


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    images = relationship(
        "BlogImage", back_populates="project", cascade="all, delete-orphan"
    )


class BlogImage(Base):
    __tablename__ = "blog_images"

    id = Column(Integer, primary_key=True, index=True)
    blog_id = Column(
        Integer, ForeignKey("blogs.id", ondelete="CASCADE"), nullable=False
    )
    link_to_disk = Column(String, nullable=False)
    public_url = Column(String, nullable=False)
    is_preview = Column(Boolean, default=False)  # 👈 Новый флаг
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    project = relationship("Blog", back_populates="images")
