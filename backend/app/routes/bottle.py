from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import db_business
from app.db import get_db_session
from app.schemas import BottleCreateRequest, BottleOut, BottlePromptOut, BottleReplyRequest

router = APIRouter(prefix="/bottles", tags=["bottles"])


@router.post("", response_model=BottleOut)
async def create_bottle(payload: BottleCreateRequest, session: AsyncSession = Depends(get_db_session)) -> BottleOut:
    return await db_business.create_bottle(session, payload.content, payload.target_gender, payload.target_scope)


@router.get("", response_model=list[BottleOut])
async def list_bottles(session: AsyncSession = Depends(get_db_session)) -> list[BottleOut]:
    return await db_business.list_bottles(session)


@router.get("/prompts/random", response_model=BottlePromptOut)
def random_bottle_prompt() -> BottlePromptOut:
    return BottlePromptOut(content=db_business.random_prompt())


@router.get("/random", response_model=BottleOut)
async def random_bottle(city: str | None = None, gender: str | None = None, age_range: str | None = None, session: AsyncSession = Depends(get_db_session)) -> BottleOut:
    return await db_business.random_bottle(session, city=city, gender=gender, age_range=age_range)


@router.post("/{bottle_id}/reply")
async def reply_bottle(bottle_id: str, payload: BottleReplyRequest, session: AsyncSession = Depends(get_db_session)) -> dict[str, str]:
    await db_business.reply_bottle(session, bottle_id, payload.content)
    return {"status": "queued", "message": "reply accepted", "content": payload.content}
