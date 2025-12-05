from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict

from api.api_v1.dependencies import require_admin
from config import settings
from core.models.db_helper import db_helper
from crud.project import (
    create_project,
    get_project,
    update_project,
    delete_project,
    add_image_to_project,
    get_image,
    delete_image,
    reorder_images, image_is_preview,
    )
from servises.storage import delete_image_file, save_image_to_yandex
from shemas.projects import ProjectRead, ProjectCreate, ImageRead, ProjectUpdate


router = APIRouter(
    dependencies=[Depends(require_admin)], prefix=settings.api.v1.admin, tags=["Admin"]
)


@router.post("/projects", response_model=ProjectRead)
async def admin_create_project(
    project: ProjectCreate, db: AsyncSession = Depends(db_helper.session_getter)
):
    new_project = await create_project(db, project)
    return new_project


@router.put("/projects/{project_id}", response_model=ProjectRead)
async def admin_update_project(
    project_id: int,
    project: ProjectUpdate,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    existing_project = await get_project(db, project_id)
    if not existing_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    updated_project = await update_project(db, project_id, project)
    return updated_project


@router.delete("/projects/{project_id}")
async def admin_delete_project(
    project_id: int, db: AsyncSession = Depends(db_helper.session_getter)
):
    project = await get_project(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    for image in project.images:
        await delete_image_file(image.file_path)
    success = await delete_project(db, project_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete project",
        )
    return {"message": "Project deleted successfully"}


@router.post("/projects/{project_id}/images", response_model=ImageRead)
async def admin_upload_image(
    project_id: int,
    file: UploadFile = File(...),
    caption: Optional[str] = Form(None),
    ordering: int = Form(0),
    db: AsyncSession = Depends(db_helper.session_getter),
):
    project = await get_project(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    file_path = await save_image_to_yandex(file, project.slug)
    link_to_disk = file_path["link_to_disk"]
    public_url = file_path["public_url"]
    image = await add_image_to_project(
        db, project_id, link_to_disk, public_url, caption, ordering
    )

    return image


@router.delete("/projects/{project_id}/images/{image_id}")
async def admin_delete_image(
    project_id: int, image_id: int, db: AsyncSession = Depends(db_helper.session_getter)
):
    image = await get_image(db, image_id)
    if not image or image.project_id != project_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found"
        )
    await delete_image_file(image.link_to_disk)
    success = await delete_image(db, image_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete image",
        )
    return {"message": "Image deleted successfully"}


@router.post("/projects/{project_id}/images/reorder")
async def admin_reorder_images(
    project_id: int,
    image_orders: Dict[int, int],
    db: AsyncSession = Depends(db_helper.session_getter),
):
    project = await get_project(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    await reorder_images(db, image_orders)
    return {"message": "Images reordered successfully"}

@router.post("/projects/{project_id}/images/ispreview/{image_id}")
async def admin_image_is_preview(
        project_id: int,
        image_id:int,
        db:AsyncSession = Depends(db_helper.session_getter)
        ):
    project = await get_project(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    await image_is_preview(db, image_id, project_id)
    return {"message": "Images is_preview successfully"}
