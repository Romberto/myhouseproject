from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config import settings
from core.models.db_helper import db_helper
from core.security.jwt import create_access_token, is_admin, verify_password
from crud.project import *
from servises.telegram_auth import verify_telegram_auth
from shemas.projects import ProjectRead, AuthResponse, PassLoginRequest, TelegramAuthData

router = APIRouter(prefix=settings.api.v1.public, tags=["public"])


@router.get("/", response_model=List[ProjectRead])
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    only_published: bool = True,
    db: AsyncSession = Depends(db_helper.session_getter)
):
    projects = await list_projects(db=db, skip=skip, limit=limit, search=search, only_published=only_published)
    return projects


@router.get("/{slug}", response_model=ProjectRead)
async def get_project_detail(slug: str, db: AsyncSession = Depends(db_helper.session_getter)):
    project = await get_project_by_slug(db, slug)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project
