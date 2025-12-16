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


class Project(Base):
    __tablename__ = "projects"

    title = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    shot_description = Column(Text, nullable=True)
    quadrature = Column(Integer)
    is_published = Column(Boolean, default=False)
    floors = Column(Integer, default=1)
    bedrooms = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    images = relationship(
        "Image", back_populates="project", cascade="all, delete-orphan"
    )


class Image(Base):
    __tablename__ = "images"

    project_id = Column(
        UUID, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    path_to_file = Column(String, nullable=False)
    public_url = Column(String, nullable=False)
    is_preview = Column(Boolean, default=False)
    is_plan = Column(Boolean, default=False)
    is_gallery = Column(Boolean, default=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    project = relationship("Project", back_populates="images")
