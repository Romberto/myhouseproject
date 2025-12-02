import io
import os
import uuid
from pathlib import Path
from pprint import pprint

from fastapi import UploadFile, HTTPException
import yadisk
import uuid
from webdav3.client import Client
from config import settings

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
    # Папка проекта на Яндекс.Диске
    remote_dir = f"/projects/{project_slug}"

    # Создаём папку, если её нет
    if not await y.exists(remote_dir):
        await y.mkdir(remote_dir)

    # Задаём уникальное имя файла
    file_ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_ext}"
    remote_path = f"{remote_dir}/{filename}"

    # Читаем содержимое файла в поток BytesIO
    content = await file.read()
    file_like = io.BytesIO(content)

    # Загружаем файл
    await y.upload(file_like, remote_path)

    # Делаем файл публичным и получаем ссылку

    file = await y.publish(remote_path)
    meta = await y.get_meta(remote_path)

    # Вот здесь правильный доступ
    public_url = await  meta.get_download_link()
    return {'link_to_disk': str(file.path), "public_url": str(public_url)}

#
# def delete_image_file(file_path: str) -> None:
#     if file_path.startswith("/storage/images/"):
#         full_path = Path(settings.storage.path) / file_path.replace(
#             "/storage/images/", ""
#         )
#         if full_path.exists():
#             full_path.unlink()
from urllib.parse import urlparse, unquote

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
