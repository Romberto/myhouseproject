from typing import List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.config import settings
from src.core.models.db_helper import db_helper
from src.shemas.projects import (
    ProjectRead,
)

router = APIRouter(prefix=settings.api.v1.public, tags=["public"])


@router.get("/", response_model=List[ProjectRead])
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    only_published: bool = True,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    projects = await list_projects(
        db=db, skip=skip, limit=limit, search=search, only_published=only_published
    )
    return projects


@router.get("/{slug}", response_model=ProjectRead)
async def get_project_detail(
    slug: str, db: AsyncSession = Depends(db_helper.session_getter)
):
    project = await get_project_by_slug(db, slug)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return project
