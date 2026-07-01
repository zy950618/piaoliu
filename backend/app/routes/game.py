from typing import Literal

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import db_business
from app.db import get_db_session
from app.schemas import GamePromptOut, GameRandomMatchRequest, GameRandomMatchResponse

router = APIRouter(prefix="/game", tags=["game"])


@router.get("/prompts/random", response_model=GamePromptOut)
async def random_game_prompt(
    mode: Literal["truth_public", "truth_private", "dare_public", "dare_private"],
    session: AsyncSession = Depends(get_db_session),
) -> GamePromptOut:
    return await db_business.random_game_prompt(session, mode)


@router.post("/random-match", response_model=GameRandomMatchResponse)
async def random_game_match(
    payload: GameRandomMatchRequest,
    session: AsyncSession = Depends(get_db_session),
) -> GameRandomMatchResponse:
    return await db_business.create_game_random_match(session, payload)
