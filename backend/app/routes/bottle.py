from fastapi import APIRouter

from app import mock_store
from app.schemas import BottleCreateRequest, BottleOut, BottlePromptOut, BottleReplyRequest

router = APIRouter(prefix="/bottles", tags=["bottles"])


@router.post("", response_model=BottleOut)
def create_bottle(payload: BottleCreateRequest) -> BottleOut:
    return mock_store.create_bottle(
        payload.content,
        target_gender=payload.target_gender,
        target_scope=payload.target_scope,
    )


@router.get("", response_model=list[BottleOut])
def list_bottles() -> list[BottleOut]:
    return mock_store.list_bottles()


@router.get("/prompts/random", response_model=BottlePromptOut)
def random_bottle_prompt() -> BottlePromptOut:
    return BottlePromptOut(content=mock_store.random_bottle_prompt())


@router.get("/random", response_model=BottleOut)
def random_bottle(city: str | None = None, gender: str | None = None, age_range: str | None = None) -> BottleOut:
    return mock_store.fish_bottle(city=city, gender=gender, age_range=age_range)


@router.post("/{bottle_id}/reply")
def reply_bottle(bottle_id: str, payload: BottleReplyRequest) -> dict[str, str]:
    for bottle in mock_store.bottles:
        if bottle.id == bottle_id:
            bottle.replies += 1
            break
    return {"status": "queued", "message": "reply accepted", "content": payload.content}
