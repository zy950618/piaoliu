from fastapi import APIRouter

from app.object_storage import prepare_upload
from app.schemas import UploadPrepareRequest, UploadPrepareResponse


router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("/prepare", response_model=UploadPrepareResponse)
async def create_upload_ticket(payload: UploadPrepareRequest) -> UploadPrepareResponse:
    return await prepare_upload(payload)
