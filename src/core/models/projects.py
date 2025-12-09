from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.core.models.base import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # images = relationship(
    #     "Image", back_populates="project", cascade="all, delete-orphan"
    # )


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    link_to_disk = Column(String, nullable=False)
    public_url = Column(String, nullable=False)
    caption = Column(String, nullable=True)
    ordering = Column(Integer, default=0)
    is_preview = Column(Boolean, default=False)  # 👈 Новый флаг
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    # project = relationship("Project", back_populates="images")
