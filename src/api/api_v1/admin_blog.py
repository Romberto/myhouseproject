from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict

from src.api.api_v1.dependencies import require_admin
from src.config import settings
from src.core.models.db_helper import db_helper
from src.crud.blog import (
    create_blog,
    get_blog_by_id,
    update_blog,
    delete_blog,

)
from src.servises.storage import s3, delete_file_storage

from src.shemas.blog import BlogCreate, BlogRead, BlogUpdate


router = APIRouter(
    dependencies=[Depends(require_admin)],
    prefix=settings.api.v1.admin,
    tags=["admin_blog"],
)


@router.post("/blogs", response_model=BlogRead)
async def admin_create_blog(
    project: BlogCreate, db: AsyncSession = Depends(db_helper.session_getter)
):
    new_blog = await create_blog(db, project)
    return new_blog


@router.put("/blogs/{blog_id}", response_model=BlogRead)
async def admin_update_blog(
    blog_id: int,
    blog: BlogUpdate,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    existing_project = await get_blog_by_id(db, blog_id)
    if not existing_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )
    updated_project = await update_blog(db, blog_id, blog)
    return updated_project


@router.delete("/blogs/{blog_id}")
async def admin_delete_blog(
    blog_id: int, db: AsyncSession = Depends(db_helper.session_getter)
):
    blog = await get_blog_by_id(db, blog_id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )
    for image in blog.images:
        remove_storage_file = await delete_file_storage(image.path_to_file)
        if not remove_storage_file:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete image",
            )
    success = await delete_blog(db, blog_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete blog",
        )
    return {"message": "Blog deleted successfully"}


# @router.post("/blogs/{blog_id}/images", response_model=BlogImageRead)
# async def admin_upload_image(
#     blog_id: int,
#     payload: ImageCreate,
#     db: AsyncSession = Depends(db_helper.session_getter),
# ):
#     blog = await get_blog_by_id(db, blog_id)
#     if not blog:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
#         )
#     path_to_file = payload.path_to_file
#     public_url = payload.public_url
#     image = await add_image_to_blog(db, blog_id, path_to_file, public_url)
#
#     return image
#

