from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import db_business
from app.db import get_db_session
from app.schemas import CheckinState

router = APIRouter(prefix="/checkin", tags=["checkin"])


@router.post("", response_model=CheckinState)
async def post_checkin(session: AsyncSession = Depends(get_db_session)) -> CheckinState:
    return await db_business.checkin_today(session)


@router.get("/week", response_model=CheckinState)
async def get_checkin_week(session: AsyncSession = Depends(get_db_session)) -> CheckinState:
    return (await db_business.get_status(session)).checkin
