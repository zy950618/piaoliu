from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import db_business
from app.db import get_db_session
from app.schemas import BlockOut, BlockRequest, ReportOut, ReportRequest

router = APIRouter(tags=["moderation"])


@router.get("/reports", response_model=list[ReportOut])
async def list_reports(session: AsyncSession = Depends(get_db_session)) -> list[ReportOut]:
    return await db_business.list_reports(session)


@router.post("/reports", response_model=ReportOut)
async def create_report(payload: ReportRequest, session: AsyncSession = Depends(get_db_session)) -> ReportOut:
    return await db_business.create_report(session, payload.target_type, payload.target_id, payload.reason)


@router.get("/blocks", response_model=list[BlockOut])
async def list_blocks(session: AsyncSession = Depends(get_db_session)) -> list[BlockOut]:
    return await db_business.list_blocks(session)


@router.post("/blocks", response_model=BlockOut)
async def block_user(payload: BlockRequest, session: AsyncSession = Depends(get_db_session)) -> BlockOut:
    return await db_business.block_user(session, payload.blocked_user_id)
