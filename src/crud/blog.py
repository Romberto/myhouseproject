from typing import Optional, List
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from src.core.models.blog import Blog
from src.shemas.blog import BlogCreate, BlogUpdate, BlogImageUpload


async def create_blog(db: AsyncSession, blog_data: BlogCreate) -> Blog:
    blog = Blog(**blog_data.model_dump())
    db.add(blog)
    await db.commit()
    await db.refresh(blog)
    return blog


async def get_blog_by_id(db: AsyncSession, blog_id: UUID) -> Optional[Blog]:
    result = await db.execute(
        select(Blog).options(selectinload(Blog.images)).where(Blog.id == blog_id)
    )
    return result.scalar_one_or_none()


async def get_blog_by_slug(db: AsyncSession, slug: str) -> Optional[Blog]:
    result = await db.execute(
        select(Blog).where(Blog.slug == slug)
    )
    return result.scalar_one_or_none()


from sqlalchemy import select, cast, String
from typing import Optional, List

async def list_blogs(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    only_published: bool = False,
) -> List[Blog]:
    query = select(Blog)

    if only_published:
        query = query.where(Blog.is_published == True)

    if search:
        query = query.where(cast(Blog.category, String).ilike(f"%{search}%"))

    query = query.offset(skip).limit(limit).order_by(Blog.created_at.desc())

    result = await db.execute(query)
    return list(result.scalars().all())



async def update_blog(
    db: AsyncSession, blog_id: UUID, blog_data: BlogUpdate
) -> Optional[Blog]:
    update_data = blog_data.model_dump(exclude_unset=True)
    if update_data:
        await db.execute(update(Blog).where(Blog.id == blog_id).values(**update_data))
        await db.commit()
    return await get_blog_by_id(db, blog_id)


async def delete_blog(db: AsyncSession, blog_id: UUID) -> bool:
    result = await db.execute(delete(Blog).where(Blog.id == blog_id))
    await db.commit()
    return result.rowcount > 0

async  def add_image_to_blog(db: AsyncSession,  blog_id: UUID, payload:BlogImageUpload):
    blog = await get_blog_by_id(db, blog_id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
            )
    if payload.path_to_file is not None:
        blog.path_to_file = payload.path_to_file

    if payload.public_url is not None:
        blog.public_url = payload.public_url

    await db.commit()
    await db.refresh(blog)
    return blog



