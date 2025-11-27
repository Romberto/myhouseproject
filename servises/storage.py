import os
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException

from config import settings

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
MAX_FILE_SIZE = 10 * 1024 * 1024


def get_file_extension(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def validate_image(file: UploadFile) -> None:
    ext = get_file_extension(file.filename or "")
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Invalid file extension. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")


async def save_image(file: UploadFile, project_slug: str) -> str:
    validate_image(file)

    project_dir = Path(settings.storage.path) / project_slug
    project_dir.mkdir(parents=True, exist_ok=True)

    ext = get_file_extension(file.filename or "")
    filename = f"{uuid.uuid4()}.{ext}"
    file_path = project_dir / filename

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")

    with open(file_path, "wb") as f:
        f.write(content)

    return f"/storage/images/{project_slug}/{filename}"


def delete_image_file(file_path: str) -> None:
    if file_path.startswith("/storage/images/"):
        full_path = Path(settings.STORAGE_PATH) / file_path.replace("/storage/images/", "")
        if full_path.exists():
            full_path.unlink()
