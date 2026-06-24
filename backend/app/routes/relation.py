from fastapi import APIRouter

from app import mock_store
from app.schemas import RelationRequest

router = APIRouter(prefix="/relations", tags=["relations"])


@router.post("/follow")
def follow_user(payload: RelationRequest) -> dict[str, str]:
    mock_store.following_user_ids.add(payload.target_user_id)
    return {"status": "followed", "target_user_id": payload.target_user_id}


@router.post("/friend-request")
def request_friend(payload: RelationRequest) -> dict[str, str]:
    return {"status": "requested", "target_user_id": payload.target_user_id}
