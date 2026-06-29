from uuid import uuid4

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import db_business
from app.db import get_db_session
from app.schemas import QuotaType, TruthQuestionOut

router = APIRouter(prefix="/truth", tags=["truth"])


@router.get("/questions", response_model=list[TruthQuestionOut])
async def list_truth_questions(session: AsyncSession = Depends(get_db_session)) -> list[TruthQuestionOut]:
    return await db_business.list_truth_questions(session)


@router.get("/question/random", response_model=TruthQuestionOut)
async def random_truth_question(session: AsyncSession = Depends(get_db_session)) -> TruthQuestionOut:
    await db_business.consume_quota(session, QuotaType.truth, f"truth:{uuid4().hex}")
    return await db_business.random_truth_question(session)
