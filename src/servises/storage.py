import boto3
from botocore.client import Config

from src.config import settings

s3 = boto3.client(
    "s3",
    endpoint_url="https://s3.twcstorage.ru",
    aws_access_key_id=settings.storage.access_key,
    aws_secret_access_key=settings.storage.secret_access_key,
    config=Config(signature_version="s3v4"),
    region_name="ru-1",
)
