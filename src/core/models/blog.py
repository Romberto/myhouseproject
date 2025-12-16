from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    UUID,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.core.models.base import Base


class Blog(Base):
    __tablename__ = "blogs"

    title = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    shot_description = Column(Text, nullable=True)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # images = relationship(
    #     "BlogImage", back_populates="project", cascade="all, delete-orphan"
    # )


class BlogImage(Base):
    __tablename__ = "blog_images"

    blog_id = Column(UUID, ForeignKey("blogs.id", ondelete="CASCADE"), nullable=False)
    path_to_file = Column(String, nullable=False)
    public_url = Column(String, nullable=False)
    is_preview = Column(Boolean, default=False)  # 👈 Новый флаг
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

    # project = relationship("Blog", back_populates="images")
