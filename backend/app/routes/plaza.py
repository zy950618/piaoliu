from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import db_business
from app.db import get_db_session
from app.schemas import NearbyUser, PlazaCommentOut, PlazaCommentRequest, PlazaCreateRequest, PlazaPost

router = APIRouter(tags=["plaza"])


@router.get("/plaza/posts", response_model=list[PlazaPost])
async def list_plaza_posts(
    city: str | None = None,
    gender: str | None = None,
    age_range: str | None = None,
    session: AsyncSession = Depends(get_db_session),
) -> list[PlazaPost]:
    return await db_business.list_plaza(session, city=city, gender=gender, age_range=age_range)


@router.get("/plaza/posts/{post_id}", response_model=PlazaPost)
async def get_plaza_post(post_id: str, session: AsyncSession = Depends(get_db_session)) -> PlazaPost:
    return await db_business.get_plaza(session, post_id)


@router.post("/plaza/posts", response_model=PlazaPost)
async def create_plaza_post(payload: PlazaCreateRequest, session: AsyncSession = Depends(get_db_session)) -> PlazaPost:
    return await db_business.create_plaza(session, payload.content, payload.media_type, payload.media_count, payload.media)


@router.post("/plaza/posts/{post_id}/comments", response_model=PlazaPost)
async def comment_plaza_post(post_id: str, payload: PlazaCommentRequest, session: AsyncSession = Depends(get_db_session)) -> PlazaPost:
    return await db_business.comment_plaza(session, post_id, payload.content, payload.hidden_for_owner_only)


@router.get("/plaza/posts/{post_id}/comments", response_model=list[PlazaCommentOut])
async def list_plaza_comments(post_id: str, viewer_id: str | None = None, session: AsyncSession = Depends(get_db_session)) -> list[PlazaCommentOut]:
    return await db_business.list_plaza_comments(session, post_id, viewer_id)


@router.post("/plaza/posts/{post_id}/like", response_model=PlazaPost)
async def like_plaza_post(post_id: str, session: AsyncSession = Depends(get_db_session)) -> PlazaPost:
    return await db_business.like_plaza(session, post_id)


@router.get("/nearby/users", response_model=list[NearbyUser])
async def list_nearby_users(
    gender: str | None = None,
    age_range: str | None = None,
    distance_km: float | None = None,
    session: AsyncSession = Depends(get_db_session),
) -> list[NearbyUser]:
    return await db_business.list_nearby(session, gender=gender, age_range=age_range, distance_km=distance_km)
