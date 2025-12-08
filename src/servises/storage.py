import io

from PIL import Image as PILImage
from fastapi import UploadFile, HTTPException
import yadisk
import uuid
from src.config import settings

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
MAX_FILE_SIZE = 10 * 1024 * 1024


def get_file_extension(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def validate_image(file: UploadFile) -> None:
    ext = get_file_extension(file.filename or "")
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file extension. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )


y = yadisk.AsyncClient(token=settings.yandex.token)  # <-- сюда токен


async def save_image_to_yandex(file: UploadFile, project_slug: str) -> dict:
    # Папка проекта на Яндекс
    validate_image(file)
    remote_dir = f"/projects/{project_slug}"

    # Создаём папку, если её нет
    if not await y.exists(remote_dir):
        await y.mkdir(remote_dir)

    # Читаем содержимое файла
    content = await file.read()
    img = PILImage.open(io.BytesIO(content))

    # --- 1. Ограничиваем размер (resize) ---
    max_size = (1600, 1600)
    img.thumbnail(max_size, PILImage.LANCZOS)

    # --- 2. Сохраняем как WEBP (лучшее сжатие) ---
    compressed_io = io.BytesIO()
    img.save(
        compressed_io,
        format="WEBP",
        quality=70,
        method=6,
    )
    compressed_io.seek(0)

    # Задаём уникальное имя файла
    file_ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_ext}"
    remote_path = f"{remote_dir}/{filename}"

    await y.upload(compressed_io, remote_path)

    # Делаем файл публичным и получаем ссылку

    file = await y.publish(remote_path)
    meta = await y.get_meta(remote_path)

    # Вот здесь правильный доступ
    public_url = await meta.get_download_link()
    return {"link_to_disk": str(file.path), "public_url": str(public_url)}


async def delete_image_file(file_path: str) -> None:
    """
    Удаляет файл с Яндекс.Диска.
    В `file_path` передаётся публичная ссылка, полученная через y.get_download_link().
    """

    if not file_path:
        return

    try:
        await y.remove(file_path)

    except Exception as e:
        print(f"Ошибка удаления файла: {e}")
