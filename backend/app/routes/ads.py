from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import db_business
from app.db import get_db_session
from app.schemas import AdCommitRequest, AdPrepareResponse, AdRewardState, MeStatus

router = APIRouter(prefix="/ads/reward", tags=["ads"])


@router.get("/status", response_model=AdRewardState)
async def reward_status(session: AsyncSession = Depends(get_db_session)) -> AdRewardState:
    return (await db_business.get_status(session)).ad_reward


@router.post("/prepare", response_model=AdPrepareResponse)
async def reward_prepare(session: AsyncSession = Depends(get_db_session)) -> AdPrepareResponse:
    return AdPrepareResponse(reward_session_id=await db_business.prepare_ad_reward(session), reward_per_quota=10)


@router.post("/commit", response_model=MeStatus)
async def reward_commit(payload: AdCommitRequest, session: AsyncSession = Depends(get_db_session)) -> MeStatus:
    return await db_business.commit_ad_reward(session, payload.reward_session_id, payload.completed)
