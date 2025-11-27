from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from typing import List, Optional

from core.models.projects import Project, Image
from shemas.projects import ProjectCreate, ProjectUpdate


async def create_project(db: AsyncSession, project_data: ProjectCreate) -> Project:
    project = Project(**project_data.model_dump())
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


async def get_project(db: AsyncSession, project_id: int) -> Optional[Project]:
    result = await db.execute(
        select(Project)
        .options(selectinload(Project.images))
        .where(Project.id == project_id)
    )
    return result.scalar_one_or_none()


async def get_project_by_slug(db: AsyncSession, slug: str) -> Optional[Project]:
    result = await db.execute(
        select(Project)
        .options(selectinload(Project.images))
        .where(Project.slug == slug)
    )
    return result.scalar_one_or_none()


async def list_projects(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    only_published: bool = False
) -> List[Project]:
    query = select(Project).options(selectinload(Project.images))

    if only_published:
        query = query.where(Project.is_published == True)

    if search:
        query = query.where(Project.title.ilike(f"%{search}%"))

    query = query.offset(skip).limit(limit).order_by(Project.created_at.desc())

    result = await db.execute(query)
    return list(result.scalars().all())


async def update_project(db: AsyncSession, project_id: int, project_data: ProjectUpdate) -> Optional[Project]:
    update_data = project_data.model_dump(exclude_unset=True)
    if update_data:
        await db.execute(update(Project).where(Project.id == project_id).values(**update_data))
        await db.commit()
    return await get_project(db, project_id)


async def delete_project(db: AsyncSession, project_id: int) -> bool:
    result = await db.execute(delete(Project).where(Project.id == project_id))
    await db.commit()
    return result.rowcount > 0


async def add_image_to_project(
    db: AsyncSession,
    project_id: int,
    file_path: str,
    caption: Optional[str] = None,
    ordering: int = 0
) -> Image:
    image = Image(project_id=project_id, file_path=file_path, caption=caption, ordering=ordering)
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image


async def get_image(db: AsyncSession, image_id: int) -> Optional[Image]:
    result = await db.execute(select(Image).where(Image.id == image_id))
    return result.scalar_one_or_none()


async def delete_image(db: AsyncSession, image_id: int) -> bool:
    result = await db.execute(delete(Image).where(Image.id == image_id))
    await db.commit()
    return result.rowcount > 0


async def reorder_images(db: AsyncSession, image_orders: dict) -> bool:
    for image_id, ordering in image_orders.items():
        await db.execute(update(Image).where(Image.id == int(image_id)).values(ordering=ordering))
    await db.commit()
    return True
