import asyncio
from datetime import timedelta
from pathlib import PurePath
from uuid import uuid4

from fastapi import HTTPException
from minio import Minio

from app import db_business
from app.schemas import UploadPrepareRequest, UploadPrepareResponse
from app.settings import get_settings


settings = get_settings()


def configured() -> bool:
    return bool(settings.object_storage_access_key and settings.object_storage_secret_key)


def safe_extension(filename: str) -> str:
    suffix = PurePath(filename).suffix.lower()
    return suffix if suffix in {".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mp3", ".m4a"} else ""


async def prepare_upload(payload: UploadPrepareRequest) -> UploadPrepareResponse:
    if not configured():
        raise HTTPException(
            status_code=503,
            detail={"code": "OBJECT_STORAGE_UNCONFIGURED", "message": "媒体存储尚未配置，请联系管理员后重试"},
        )
    user_id = db_business.current_user_id()
    object_key = f"users/{user_id}/{uuid4().hex}{safe_extension(payload.filename)}"
    client = Minio(
        settings.object_storage_endpoint,
        access_key=settings.object_storage_access_key,
        secret_key=settings.object_storage_secret_key,
        secure=settings.object_storage_secure,
    )

    def issue_url() -> str:
        if not client.bucket_exists(settings.object_storage_bucket):
            client.make_bucket(settings.object_storage_bucket)
        return client.presigned_put_object(settings.object_storage_bucket, object_key, expires=timedelta(minutes=15))

    try:
        upload_url = await asyncio.to_thread(issue_url)
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail={"code": "OBJECT_STORAGE_UNAVAILABLE", "message": "媒体存储暂时不可用，请稍后重试"},
        ) from exc
    public_url = f"{settings.object_storage_public_endpoint.rstrip('/')}/{settings.object_storage_bucket}/{object_key}"
    return UploadPrepareResponse(
        object_key=object_key,
        upload_url=upload_url,
        public_url=public_url,
        expires_in_seconds=900,
    )
