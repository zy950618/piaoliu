from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import db_business
from app.db import get_db_session
from app.schemas import MeStatus, UserActivityRecordCreateRequest, UserActivityRecordOut, UserProfile, UserProfileUpdateRequest, UserRecordSummaryItem

router = APIRouter(tags=["me"])


@router.get("/me/status", response_model=MeStatus)
async def me_status(session: AsyncSession = Depends(get_db_session)) -> MeStatus:
    return await db_business.get_status(session)


@router.get("/users/me/status", response_model=MeStatus)
async def user_status(session: AsyncSession = Depends(get_db_session)) -> MeStatus:
    return await db_business.get_status(session)


@router.patch("/me/profile", response_model=UserProfile)
async def update_me_profile(payload: UserProfileUpdateRequest, session: AsyncSession = Depends(get_db_session)) -> UserProfile:
    return await db_business.update_profile(session, payload)


@router.post("/me/profile", response_model=UserProfile)
async def save_me_profile(payload: UserProfileUpdateRequest, session: AsyncSession = Depends(get_db_session)) -> UserProfile:
    return await db_business.update_profile(session, payload)


@router.get("/me/records", response_model=list[UserRecordSummaryItem])
async def my_records(session: AsyncSession = Depends(get_db_session)) -> list[UserRecordSummaryItem]:
    return await db_business.list_user_record_summaries(session)


@router.post("/me/records", response_model=UserActivityRecordOut)
async def create_my_record(payload: UserActivityRecordCreateRequest, session: AsyncSession = Depends(get_db_session)) -> UserActivityRecordOut:
    return await db_business.create_user_activity_record(session, payload)
