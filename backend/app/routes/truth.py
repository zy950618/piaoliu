from random import choice
from uuid import uuid4

from fastapi import APIRouter

from app.mock_store import consume_quota, truth_questions
from app.schemas import QuotaType, TruthQuestionOut

router = APIRouter(prefix="/truth", tags=["truth"])


@router.get("/questions", response_model=list[TruthQuestionOut])
def list_truth_questions() -> list[TruthQuestionOut]:
    return truth_questions


@router.get("/question/random", response_model=TruthQuestionOut)
def random_truth_question() -> TruthQuestionOut:
    consume_quota(QuotaType.truth, f"truth:{uuid4().hex}")
    return choice(truth_questions)
