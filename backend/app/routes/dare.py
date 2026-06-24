from random import choice
from uuid import uuid4

from fastapi import APIRouter

from app.mock_store import consume_quota, dare_tasks
from app.schemas import DareTaskOut, QuotaType

router = APIRouter(prefix="/dare", tags=["dare"])


@router.get("/tasks", response_model=list[DareTaskOut])
def list_dare_tasks() -> list[DareTaskOut]:
    return dare_tasks


@router.get("/task/random", response_model=DareTaskOut)
def random_dare_task() -> DareTaskOut:
    consume_quota(QuotaType.dare, f"dare:{uuid4().hex}")
    return choice(dare_tasks)
