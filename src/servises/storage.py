import io

from PIL import Image as PILImage
from fastapi import UploadFile, HTTPException
import yadisk
import uuid
from src.config import settings
from supabase import create_client


ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
MAX_FILE_SIZE = 10 * 1024 * 1024
SUPABASE_URL=settings.supabase.url
SUPABASE_KEY=settings.supabase.key

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def get_file_extension(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def validate_image(file: UploadFile) -> None:
    ext = get_file_extension(file.filename or "")
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file extension. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )


