from typing import Optional, List

from fastapi import HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from src.core.models.blog import Blog, BlogImage
from src.shemas.blog import BlogCreate, BlogUpdate


async def create_blog(db: AsyncSession, project_data: BlogCreate) -> Blog:
    project = Blog(**project_data.model_dump())
    db.add(project)
    await db.commit()

    stmt = (
        select(Blog)
        .options(selectinload(Blog.images))  # 👈 Загрузка связанных изображений
        .where(Blog.id == project.id)
    )
    result = await db.execute(stmt)
    return result.scalar_one()


async def get_blog_by_id(db: AsyncSession, blog_id: int) -> Optional[Blog]:
    result = await db.execute(
        select(Blog).options(selectinload(Blog.images)).where(Blog.id == blog_id)
    )
    return result.scalar_one_or_none()


async def get_blog_by_slug(db: AsyncSession, slug: str) -> Optional[Blog]:
    result = await db.execute(
        select(Blog).options(selectinload(Blog.images)).where(Blog.slug == slug)
    )
    return result.scalar_one_or_none()


async def list_blogs(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    only_published: bool = False,
) -> List[Blog]:
    query = select(Blog).options(selectinload(Blog.images))

    if only_published:
        query = query.where(Blog.is_published == True)

    if search:
        query = query.where(Blog.title.ilike(f"%{search}%"))

    query = query.offset(skip).limit(limit).order_by(Blog.created_at.desc())

    result = await db.execute(query)
    return list(result.scalars().all())


async def update_blog(
    db: AsyncSession, blog_id: int, project_data: BlogUpdate
) -> Optional[Blog]:
    update_data = project_data.model_dump(exclude_unset=True)
    if update_data:
        await db.execute(update(Blog).where(Blog.id == blog_id).values(**update_data))
        await db.commit()
    return await get_blog_by_id(db, blog_id)


async def delete_blog(db: AsyncSession, blog_id: int) -> bool:
    result = await db.execute(delete(Blog).where(Blog.id == blog_id))
    await db.commit()
    return result.rowcount > 0


async def add_image_to_blog(
    db: AsyncSession,
    project_id: int,
    link_to_disk: str,
    public_url: str,
) -> BlogImage:
    image = BlogImage(
        project_id=project_id,
        link_to_disk=link_to_disk,
        public_url=public_url,
    )
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image


async def get_blog_image(db: AsyncSession, image_id: int) -> Optional[BlogImage]:
    result = await db.execute(select(BlogImage).where(BlogImage.id == image_id))
    return result.scalar_one_or_none()


async def delete_blog_image(db: AsyncSession, image_id: int) -> bool:
    result = await db.execute(delete(BlogImage).where(BlogImage.id == image_id))
    await db.commit()
    return result.rowcount > 0


async def blog_image_is_preview(db: AsyncSession, image_id: int, project_id) -> bool:
    # Проверяем, что изображение принадлежит проекту
    q = select(BlogImage).where(
        BlogImage.id == image_id, BlogImage.project_id == project_id
    )
    result = await db.execute(q)
    image = result.scalar_one_or_none()

    if image is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found for this project",
        )

    # 1. Сбрасываем у всех изображений проекта is_preview = False
    await db.execute(
        update(BlogImage)
        .where(BlogImage.project_id == project_id)
        .values(is_preview=False)
    )

    # 2. Устанавливаем превью для выбранного изображения
    await db.execute(
        update(BlogImage).where(BlogImage.id == image_id).values(is_preview=True)
    )

    # Применяем изменения
    await db.commit()

    return True
