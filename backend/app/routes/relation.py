from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import db_business
from app.db import get_db_session
from app.schemas import RelationRequest

router = APIRouter(prefix="/relations", tags=["relations"])


@router.post("/follow")
async def follow_user(payload: RelationRequest, session: AsyncSession = Depends(get_db_session)) -> dict[str, str]:
    return await db_business.follow_user(session, payload.target_user_id)


@router.post("/friend-request")
async def request_friend(payload: RelationRequest, session: AsyncSession = Depends(get_db_session)) -> dict[str, str]:
    return await db_business.request_friend(session, payload.target_user_id)
