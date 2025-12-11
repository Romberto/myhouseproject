from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict

from src.api.api_v1.dependencies import require_admin
from src.config import settings
from src.core.models.db_helper import db_helper
from src.crud.blog import create_blog, get_blog_by_id, update_blog, delete_blog, add_image_to_blog, get_blog_image, \
    delete_blog_image, blog_image_is_preview
from src.servises.storage import delete_image_file, save_image_to_yandex
from src.shemas.blog import BlogCreate, BlogRead, BlogUpdate, BlogImageRead

router = APIRouter(
    dependencies=[Depends(require_admin)], prefix=settings.api.v1.admin, tags=["admin_blog"]
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
        await delete_image_file(image.link_to_disk)
    success = await delete_blog(db, blog_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete blog",
        )
    return {"message": "Blog deleted successfully"}


@router.post("/blogs/{blog_id}/images", response_model=BlogImageRead)
async def admin_upload_image(
    blog_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(db_helper.session_getter),
):
    blog = await get_blog_by_id(db, blog_id)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    file_path = await save_image_to_yandex(file, blog.slug)
    link_to_disk = file_path["link_to_disk"]
    public_url = file_path["public_url"]
    image = await add_image_to_blog(
        db, blog_id, link_to_disk, public_url
    )

    return image


@router.delete("/blogs/{blog_id}/images/{image_id}")
async def admin_delete_blog_image(
    blog_id: int, image_id: int, db: AsyncSession = Depends(db_helper.session_getter)
):
    image = await get_blog_image(db, image_id)
    if not image or image.blog_id != blog_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="BlogImage not found"
        )
    await delete_image_file(image.link_to_disk)
    success = await delete_blog_image(db, image_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete image",
        )
    return {"message": "BlogImage deleted successfully"}

@router.post("/blogs/{blog_id}/images/ispreview/{image_id}")
async def admin_blog_image_is_preview(
    blog_id: int, image_id: int, db: AsyncSession = Depends(db_helper.session_getter)
):
    project = await get_blog_image(db, blog_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
        )
    await blog_image_is_preview(db, image_id, blog_id)
    return {"message": "BlogImages is_preview successfully"}
