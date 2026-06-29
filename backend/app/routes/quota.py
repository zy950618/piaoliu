from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import db_business
from app.db import get_db_session
from app.schemas import ConsumeQuotaRequest, QuotaItem, QuotaType

router = APIRouter(prefix="/quota", tags=["quota"])


@router.get("/today", response_model=dict[QuotaType, QuotaItem])
async def quota_today(session: AsyncSession = Depends(get_db_session)) -> dict[QuotaType, QuotaItem]:
    return (await db_business.get_status(session)).quotas


@router.post("/consume", response_model=QuotaItem)
async def quota_consume(payload: ConsumeQuotaRequest, session: AsyncSession = Depends(get_db_session)) -> QuotaItem:
    return await db_business.consume_quota(session, payload.quota_type, payload.business_id)
