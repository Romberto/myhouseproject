from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    Enum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.core.models.base import Base
import enum


class BlogCategory(enum.Enum):
    tips = "tips"
    analytics = "analytics"
    technologies = "technologies"


class Blog(Base):
    __tablename__ = "blogs"

    title = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)
    category = Column(
        Enum(
            BlogCategory,
            name="blog_category_enum",  # имя ENUM в БД
        ),
        nullable=False,
        default=BlogCategory.tips,
    )
    article = Column(Text, nullable=True)  # статья
    excerpt = Column(Text, nullable=True)  # короткое описание
    path_to_file = Column(String, nullable=True)  # путь для файла превью
    public_url = Column(String, nullable=True)  # публичная ссылка на изображение статьи
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
