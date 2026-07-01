from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import db_business
from app.db import get_db_session
from app.schemas import (
    ChatAppealCreateRequest,
    ChatAppealOut,
    ConversationGiftResponse,
    ConversationGiftRequest,
    ConversationThreadOut,
    ConversationTurnCreate,
    GameRoomCreate,
    GameRoomCreateResponse,
    MessageItemOut,
)

router = APIRouter(tags=["messages"])


@router.get("/messages", response_model=list[MessageItemOut])
async def list_messages(session: AsyncSession = Depends(get_db_session)) -> list[MessageItemOut]:
    return await db_business.list_messages(session)


@router.post("/messages/read-all")
async def mark_messages_read(session: AsyncSession = Depends(get_db_session)) -> dict[str, str]:
    return await db_business.mark_messages_read(session)


@router.post("/messages/{message_id}/read", response_model=MessageItemOut)
async def mark_message_read(message_id: str, session: AsyncSession = Depends(get_db_session)) -> MessageItemOut:
    return await db_business.mark_message_read(session, message_id)


@router.get("/conversations", response_model=list[ConversationThreadOut])
async def list_conversations(session: AsyncSession = Depends(get_db_session)) -> list[ConversationThreadOut]:
    return await db_business.list_threads(session)


@router.post("/conversations/{thread_id}/read", response_model=ConversationThreadOut)
async def mark_conversation_read(thread_id: str, session: AsyncSession = Depends(get_db_session)) -> ConversationThreadOut:
    return await db_business.mark_thread_read(session, thread_id)


@router.post("/conversations/{thread_id}/appeal", response_model=ChatAppealOut)
async def create_chat_appeal(thread_id: str, payload: ChatAppealCreateRequest, session: AsyncSession = Depends(get_db_session)) -> ChatAppealOut:
    return await db_business.create_chat_appeal(session, thread_id, payload.reason)


@router.post("/conversations/{thread_id}/turns", response_model=ConversationThreadOut)
async def send_conversation_turn(thread_id: str, payload: ConversationTurnCreate, session: AsyncSession = Depends(get_db_session)) -> ConversationThreadOut:
    return await db_business.send_turn(session, thread_id, payload.body, payload.type, payload.media_url, payload.media_duration)


@router.post("/conversations/{thread_id}/turns/{turn_id}/view", response_model=ConversationThreadOut)
async def view_conversation_turn(thread_id: str, turn_id: str, session: AsyncSession = Depends(get_db_session)) -> ConversationThreadOut:
    return await db_business.mark_turn_viewed(session, thread_id, turn_id)


@router.post("/conversations/{thread_id}/rooms", response_model=GameRoomCreateResponse)
async def create_game_room(thread_id: str, payload: GameRoomCreate, session: AsyncSession = Depends(get_db_session)) -> GameRoomCreateResponse:
    room_id, thread = await db_business.create_game_room(session, thread_id, payload.mode)
    return GameRoomCreateResponse(room_id=room_id, thread=thread)


@router.post("/conversations/{thread_id}/gifts", response_model=ConversationGiftResponse)
async def send_conversation_gift(thread_id: str, payload: ConversationGiftRequest, session: AsyncSession = Depends(get_db_session)) -> ConversationGiftResponse:
    wallet, thread = await db_business.send_thread_gift(session, thread_id, payload.gift_id)
    return ConversationGiftResponse(wallet=wallet, thread=thread)
