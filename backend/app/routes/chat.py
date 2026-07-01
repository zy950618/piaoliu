from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import chat_store, db_business
from app.db import get_db_session
from app.dependencies import require_admin_role
from app.schemas import (
    ChatContextRequestAccept,
    ChatContextRequestCreate,
    ChatContextRequestOut,
    ChatContextRequestReject,
    ChatConversationBlockRequest,
    ChatConversationBlockResponse,
    ChatConversationOut,
    ChatConversationReportRequest,
    ChatConversationReportResponse,
    ChatMessageCreate,
    ChatMessageSendResponse,
    MatchExpandContextResponse,
    RelationRequest,
)
from app.security import AdminPrincipal

router = APIRouter(tags=["chat"])


@router.post("/chat/context-requests", response_model=ChatContextRequestOut)
async def create_context_request(payload: ChatContextRequestCreate, session: AsyncSession = Depends(get_db_session)) -> ChatContextRequestOut:
    return await chat_store.create_context_request(session, payload)


@router.get("/chat/context-requests", response_model=list[ChatContextRequestOut])
async def list_context_requests(status: str | None = None, session: AsyncSession = Depends(get_db_session)) -> list[ChatContextRequestOut]:
    return await chat_store.list_context_requests(session, status=status)


@router.post("/chat/match-expand-requests", response_model=MatchExpandContextResponse)
async def create_match_expand_request(payload: RelationRequest, session: AsyncSession = Depends(get_db_session)) -> MatchExpandContextResponse:
    return await db_business.create_match_expand_context_request(session, payload.target_user_id)


@router.post("/chat/context-requests/{request_id}/accept", response_model=ChatContextRequestOut)
async def accept_context_request(request_id: str, payload: ChatContextRequestAccept, session: AsyncSession = Depends(get_db_session)) -> ChatContextRequestOut:
    return await chat_store.accept_context_request(session, request_id, payload)


@router.post("/chat/context-requests/{request_id}/reject", response_model=ChatContextRequestOut)
async def reject_context_request(request_id: str, payload: ChatContextRequestReject, session: AsyncSession = Depends(get_db_session)) -> ChatContextRequestOut:
    return await chat_store.reject_context_request(session, request_id, payload.reason)


@router.get("/chat/conversations", response_model=list[ChatConversationOut])
async def list_context_conversations(status: str | None = None, source_type: str | None = None, session: AsyncSession = Depends(get_db_session)) -> list[ChatConversationOut]:
    return await chat_store.list_conversations(session, status=status, source_type=source_type)


@router.get("/chat/conversations/{conversation_id}", response_model=ChatConversationOut)
async def get_context_conversation(conversation_id: str, session: AsyncSession = Depends(get_db_session)) -> ChatConversationOut:
    return await chat_store.get_conversation(session, conversation_id)


@router.post("/chat/conversations/{conversation_id}/messages", response_model=ChatMessageSendResponse)
async def send_context_message(conversation_id: str, payload: ChatMessageCreate, session: AsyncSession = Depends(get_db_session)) -> ChatMessageSendResponse:
    return await chat_store.send_message(session, conversation_id, payload)


@router.post("/chat/conversations/{conversation_id}/report", response_model=ChatConversationReportResponse)
async def report_context_conversation(conversation_id: str, payload: ChatConversationReportRequest, session: AsyncSession = Depends(get_db_session)) -> ChatConversationReportResponse:
    return await chat_store.report_conversation(session, conversation_id, payload)


@router.post("/chat/conversations/{conversation_id}/block", response_model=ChatConversationBlockResponse)
async def block_context_conversation(conversation_id: str, payload: ChatConversationBlockRequest, session: AsyncSession = Depends(get_db_session)) -> ChatConversationBlockResponse:
    return await chat_store.block_conversation(session, conversation_id, payload)


@router.get("/admin/chat/context-requests", response_model=list[ChatContextRequestOut])
async def admin_context_requests(
    _: AdminPrincipal = Depends(require_admin_role("admin", "moderator")),
    session: AsyncSession = Depends(get_db_session),
) -> list[ChatContextRequestOut]:
    return await chat_store.admin_context_requests(session)


@router.get("/admin/chat/conversations/{conversation_id}", response_model=ChatConversationOut)
async def admin_context_conversation(
    conversation_id: str,
    _: AdminPrincipal = Depends(require_admin_role("admin", "moderator")),
    session: AsyncSession = Depends(get_db_session),
) -> ChatConversationOut:
    return await chat_store.admin_conversation(session, conversation_id)
