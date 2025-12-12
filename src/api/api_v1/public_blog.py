from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.config import settings
from src.core.models.db_helper import db_helper
from src.crud.blog import list_blogs, get_blog_by_slug
from src.shemas.blog import BlogRead

router = APIRouter(prefix=settings.api.v1.blog, tags=["public_blog"])


@router.get("/", response_model=List[BlogRead])
async def get_blogs(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    only_published: bool = True,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    projects = await list_blogs(
        db=db, skip=skip, limit=limit, search=search, only_published=only_published
    )
    return projects


@router.get("/{slug}", response_model=BlogRead)
async def get_blog_detail(
    slug: str, db: AsyncSession = Depends(db_helper.session_getter)
):
    project = await get_blog_by_slug(db, slug)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )
    return project