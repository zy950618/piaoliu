from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import db_business, relation_store
from app.db import get_db_session
from app.schemas import FriendRequestOut, FriendshipOut, RelationRequest, RelationStateOut

router = APIRouter(prefix="/relations", tags=["relations"])


@router.post("/follow")
async def follow_user(payload: RelationRequest, session: AsyncSession = Depends(get_db_session)) -> dict[str, str]:
    return await db_business.follow_user(session, payload.target_user_id)


@router.post("/friend-request")
async def request_friend(payload: RelationRequest, session: AsyncSession = Depends(get_db_session)) -> dict[str, str]:
    result = await relation_store.create_friend_request(session, payload.target_user_id)
    return {"status": result.status, "target_user_id": result.target_user_id, "request_id": result.id}


@router.get("/friend-requests", response_model=list[FriendRequestOut])
async def list_friend_requests(direction: str = "incoming", session: AsyncSession = Depends(get_db_session)) -> list[FriendRequestOut]:
    return await relation_store.list_friend_requests(session, "outgoing" if direction == "outgoing" else "incoming")


@router.post("/friend-requests/{request_id}/accept", response_model=FriendRequestOut)
async def accept_friend_request(request_id: str, session: AsyncSession = Depends(get_db_session)) -> FriendRequestOut:
    return await relation_store.resolve_friend_request(session, request_id, True)


@router.post("/friend-requests/{request_id}/reject", response_model=FriendRequestOut)
async def reject_friend_request(request_id: str, session: AsyncSession = Depends(get_db_session)) -> FriendRequestOut:
    return await relation_store.resolve_friend_request(session, request_id, False)


@router.get("/friends", response_model=list[FriendshipOut])
async def list_friends(session: AsyncSession = Depends(get_db_session)) -> list[FriendshipOut]:
    return await relation_store.list_friends(session)


@router.delete("/friends/{target_user_id}", response_model=FriendshipOut)
async def remove_friend(target_user_id: str, session: AsyncSession = Depends(get_db_session)) -> FriendshipOut:
    return await relation_store.remove_friend(session, target_user_id)


@router.get("/{target_user_id}/state", response_model=RelationStateOut)
async def get_relation_state(target_user_id: str, session: AsyncSession = Depends(get_db_session)) -> RelationStateOut:
    return await relation_store.relation_state(session, target_user_id)
