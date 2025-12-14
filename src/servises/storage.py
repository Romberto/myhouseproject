import boto3
from botocore.client import Config
from fastapi import HTTPException

from src.config import settings

s3 = boto3.client(
    "s3",
    endpoint_url="https://s3.twcstorage.ru",
    aws_access_key_id=settings.storage.access_key,
    aws_secret_access_key=settings.storage.secret_access_key,
    config=Config(signature_version="s3v4"),
    region_name="ru-1",
)


async def delete_file_storage(path_to_file: str):
    try:
        response = s3.delete_object(Bucket=settings.storage.bucket, Key=path_to_file)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")
