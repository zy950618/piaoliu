from fastapi import APIRouter

from app import mock_store
from app.schemas import BlockOut, BlockRequest, ReportOut, ReportRequest

router = APIRouter(tags=["moderation"])


@router.get("/reports", response_model=list[ReportOut])
def list_reports() -> list[ReportOut]:
    return list(mock_store.reports_by_key.values())


@router.post("/reports", response_model=ReportOut)
def create_report(payload: ReportRequest) -> ReportOut:
    return mock_store.create_report(payload.target_type, payload.target_id, payload.reason)


@router.get("/blocks", response_model=list[BlockOut])
def list_blocks() -> list[BlockOut]:
    return list(mock_store.blocks_by_user.values())


@router.post("/blocks", response_model=BlockOut)
def block_user(payload: BlockRequest) -> BlockOut:
    return mock_store.block_user(payload.blocked_user_id)
