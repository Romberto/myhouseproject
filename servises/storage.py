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
        raise HTTPException(status_code=400, detail=f"Invalid file extension. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")


# YANDEX_WEBDAV = {
#     "webdav_hostname": settings.yandex.webdav_hostname,
#     "webdav_login": settings.yandex.webdav_login,
#     "webdav_password": settings.yandex.webdav_password
# }
#
# client = Client(YANDEX_WEBDAV)



y = yadisk.YaDisk(token=settings.yandex.token)  # <-- сюда токен

async def save_image_to_yandex(file: UploadFile, project_slug: str) -> str:
    # Папка проекта на Яндекс.Диске
    remote_dir = f"/projects/{project_slug}"

    # Создаём папку, если её нет
    if not y.exists(remote_dir):
        y.mkdir(remote_dir)

    # Задаём уникальное имя файла
    file_ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_ext}"
    remote_path = f"{remote_dir}/{filename}"

    # Читаем содержимое файла в поток BytesIO
    content = await file.read()
    file_like = io.BytesIO(content)

    # Загружаем файл
    y.upload(file_like, remote_path)

    # Делаем файл публичным и получаем ссылку
    if not y.is_public_file(remote_path):
        y.publish(remote_path)
    meta = y.get_meta(remote_path)
    direct_url = meta.public_url

    return y.get_download_link(remote_path)




def delete_image_file(file_path: str) -> None:
    if file_path.startswith("/storage/images/"):
        full_path = Path(settings.storage.path) / file_path.replace("/storage/images/", "")
        if full_path.exists():
            full_path.unlink()
