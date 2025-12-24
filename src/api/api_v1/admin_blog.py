import uuid
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
    delete_blog, add_image_to_blog, delete_blog_image_to_db,

    )
from src.servises.storage import s3, delete_file_storage

from src.shemas.blog import BlogCreate, BlogRead, BlogUpdate, BlogImageUpload

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
    blog_id: uuid.UUID,
    blog: BlogUpdate,
    db: AsyncSession = Depends(db_helper.session_getter),
):
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


@router.post("/blog/{blog_id}/images", response_model=BlogRead)
async def admin_upload_blog_image(
    blog_id: uuid.UUID,
    payload: BlogImageUpload,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    _blog = await add_image_to_blog(db, blog_id, payload)
    return _blog

# @router.delete("/blogs/{blog_id}/images")
# async def delete_blog_image(db:AsyncSession, blog_id: uuid.UUID):
#     path_to_file = await delete_blog_image_to_db(db, blog_id)
#     if path_to_file:
#         remove_storage_file = await delete_file_storage(path_to_file)
#         if remove_storage_file:
#             return {'message': "success delete blog image"}
#     return {'message':'error delete blog image'}


