from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select

from app import db_business
from app.db import async_session_factory
from app.models import ChatConversationRecord, RoomMember
from app.realtime import realtime_hub
from app.settings import get_settings
from app.user_security import authenticate_user_token


router = APIRouter(tags=["realtime"])
settings = get_settings()


@router.websocket("/ws/chat/{conversation_id}")
async def chat_socket(websocket: WebSocket, conversation_id: str) -> None:
    token = websocket.query_params.get("token", "")
    session_identity = authenticate_user_token(token) if token else None
    user_id = session_identity.user_id if session_identity else None
    if user_id is None and settings.environment in {"mock", "dev", "development", "test"}:
        user_id = websocket.query_params.get("client_id")
    if not user_id:
        await websocket.close(code=4401, reason="登录状态已失效")
        return
    if async_session_factory is None:
        await websocket.close(code=1011, reason="数据库尚未就绪")
        return

    identity_token = db_business.set_current_user_id(user_id)
    try:
        async with async_session_factory() as session:
            conversation = await session.get(ChatConversationRecord, conversation_id)
            if conversation is None or user_id not in {
                conversation.participant_a_id,
                conversation.participant_b_id,
            }:
                await websocket.close(code=4404, reason="会话不存在")
                return
        await realtime_hub.connect(conversation_id, user_id, websocket)
        await websocket.send_json(
            {
                "type": "connection.ready",
                "conversation_id": conversation_id,
                "recovery": {"method": "http", "endpoint": f"/chat/conversations/{conversation_id}/messages"},
            }
        )
        while True:
            payload = await websocket.receive_json()
            if payload.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        pass
    finally:
        realtime_hub.disconnect(conversation_id, user_id, websocket)
        db_business.reset_current_user_id(identity_token)


@router.websocket("/ws/rooms/{room_id}")
async def room_socket(websocket: WebSocket, room_id: str) -> None:
    token = websocket.query_params.get("token", "")
    session_identity = authenticate_user_token(token) if token else None
    user_id = session_identity.user_id if session_identity else None
    if user_id is None and settings.environment in {"mock", "dev", "development", "test"}:
        user_id = websocket.query_params.get("client_id")
    if not user_id or async_session_factory is None:
        await websocket.close(code=4401, reason="登录状态已失效")
        return
    identity_token = db_business.set_current_user_id(user_id)
    try:
        async with async_session_factory() as session:
            member = await session.scalar(
                select(RoomMember).where(
                    RoomMember.room_id == room_id,
                    RoomMember.user_id == user_id,
                    RoomMember.status == "active",
                )
            )
            if member is None:
                await websocket.close(code=4403, reason="尚未加入房间")
                return
        await realtime_hub.connect(room_id, user_id, websocket)
        await websocket.send_json({"type": "connection.ready", "room_id": room_id})
        while True:
            payload = await websocket.receive_json()
            if payload.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        pass
    finally:
        realtime_hub.disconnect(room_id, user_id, websocket)
        db_business.reset_current_user_id(identity_token)
