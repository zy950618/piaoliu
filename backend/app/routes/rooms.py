from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import room_store
from app.db import get_db_session
from app.realtime import realtime_hub
from app.schemas import GameRoundCreate, GameRoundOut, RoomCreate, RoomInvitationCreate, RoomInvitationOut, RoomOut


router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.post("", response_model=RoomOut)
async def create_room(payload: RoomCreate, session: AsyncSession = Depends(get_db_session)) -> RoomOut:
    return await room_store.create_room(session, payload)


@router.get("", response_model=list[RoomOut])
async def list_rooms(scope: str = "mine", session: AsyncSession = Depends(get_db_session)) -> list[RoomOut]:
    return await room_store.list_rooms(session, "public" if scope == "public" else "mine")


@router.get("/invitations", response_model=list[RoomInvitationOut])
async def list_room_invitations(status: str = "pending", session: AsyncSession = Depends(get_db_session)) -> list[RoomInvitationOut]:
    return await room_store.list_invitations(session, status)


@router.get("/{room_id}", response_model=RoomOut)
async def get_room(room_id: str, session: AsyncSession = Depends(get_db_session)) -> RoomOut:
    return await room_store.get_room(session, room_id)


@router.post("/{room_id}/invitations", response_model=RoomInvitationOut)
async def invite_room_member(
    room_id: str, payload: RoomInvitationCreate, session: AsyncSession = Depends(get_db_session)
) -> RoomInvitationOut:
    return await room_store.create_invitation(session, room_id, payload)


@router.post("/invitations/{invitation_id}/accept", response_model=RoomOut)
async def accept_room_invitation(invitation_id: str, session: AsyncSession = Depends(get_db_session)) -> RoomOut:
    result = await room_store.accept_invitation(session, invitation_id)
    await realtime_hub.broadcast(result.id, {"type": "room.updated", "room_id": result.id, "status": result.status})
    return result


@router.post("/{room_id}/join", response_model=RoomOut)
async def join_public_room(room_id: str, session: AsyncSession = Depends(get_db_session)) -> RoomOut:
    result = await room_store.join_public_room(session, room_id)
    await realtime_hub.broadcast(result.id, {"type": "room.updated", "room_id": result.id, "status": result.status})
    return result


@router.post("/{room_id}/rounds", response_model=GameRoundOut)
async def create_game_round(
    room_id: str, payload: GameRoundCreate, session: AsyncSession = Depends(get_db_session)
) -> GameRoundOut:
    result = await room_store.create_game_round(session, room_id, payload)
    await realtime_hub.broadcast(room_id, {"type": "room.round.resolved", "room_id": room_id, "round": result.model_dump()})
    return result


@router.post("/{room_id}/end", response_model=RoomOut)
async def end_room(room_id: str, session: AsyncSession = Depends(get_db_session)) -> RoomOut:
    result = await room_store.dissolve_room(session, room_id)
    await realtime_hub.broadcast(room_id, {"type": "room.updated", "room_id": room_id, "status": result.status})
    return result
