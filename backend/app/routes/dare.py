from uuid import uuid4

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import db_business
from app.db import get_db_session
from app.schemas import DareTaskOut, QuotaType

router = APIRouter(prefix="/dare", tags=["dare"])


@router.get("/tasks", response_model=list[DareTaskOut])
async def list_dare_tasks(session: AsyncSession = Depends(get_db_session)) -> list[DareTaskOut]:
    return await db_business.list_dare_tasks(session)


@router.get("/task/random", response_model=DareTaskOut)
async def random_dare_task(session: AsyncSession = Depends(get_db_session)) -> DareTaskOut:
    await db_business.consume_quota(session, QuotaType.dare, f"dare:{uuid4().hex}")
    return await db_business.random_dare_task(session)
