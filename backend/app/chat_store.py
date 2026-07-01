import json
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import db_business
from app.audit import record_admin_audit
from app.models import (
    ChatContextRequestRecord,
    ChatConversationBlockRecord,
    ChatConversationRecord,
    ChatConversationReportRecord,
    ChatMessageRecord,
)
from app.schemas import (
    ChatContextRequestAccept,
    ChatContextRequestCreate,
    ChatContextRequestOut,
    ChatConversationBlockRequest,
    ChatConversationBlockResponse,
    ChatConversationOut,
    ChatConversationReportRequest,
    ChatConversationReportResponse,
    ChatMessageCreate,
    ChatMessageOut,
    ChatMessageSendResponse,
)

RISK_WORDS = {"wx": "external_contact", "wechat": "external_contact", "telegram": "external_contact", "转账": "payment_risk"}
SEED_INVITER_ID = "200000000004"

# Kept only so restart-style tests can clear previous in-memory stores; state no longer depends on these.
context_requests: dict[str, dict] = {}
conversations: dict[str, dict] = {}
blocked_pairs: set[tuple[str, str]] = set()
reports: dict[str, dict] = {}


def now() -> datetime:
    return datetime.now(UTC)


def iso(value: datetime | None) -> str | None:
    return value.isoformat() if value else None


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex}"


def current_user_id() -> str:
    return db_business.current_user_id()


def error(status_code: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"code": code, "message": message})


def source_summary(source_type: str, source_id: str | None, title: str | None = None) -> dict[str, str]:
    return {
        "title": title or "基于本次互动开启",
        "source_type": source_type,
        "source_id": source_id or "",
    }


def rate_limit(friendship_state: str = "none") -> dict[str, int | str]:
    return {"scope": friendship_state, "messages_per_minute": 20 if friendship_state == "friend" else 6}


def audit_refs_load(value: str | None) -> list[str]:
    if not value:
        return []
    try:
        result = json.loads(value)
    except json.JSONDecodeError:
        return []
    return result if isinstance(result, list) else []


def audit_refs_dump(value: list[str]) -> str:
    return json.dumps(value, ensure_ascii=False)


def participants(row: ChatContextRequestRecord | ChatConversationRecord) -> list[str]:
    if isinstance(row, ChatContextRequestRecord):
        return [row.initiator_id, row.target_user_id]
    return [row.participant_a_id, row.participant_b_id]


async def ensure_participant(row: ChatConversationRecord) -> None:
    if current_user_id() not in participants(row):
        raise error(404, "CHAT_CONVERSATION_NOT_FOUND", "Conversation not found")


async def blocked_between(session: AsyncSession, user_a: str, user_b: str) -> bool:
    row = await session.scalar(
        select(ChatConversationBlockRecord).where(
            or_(
                (ChatConversationBlockRecord.blocker_id == user_a) & (ChatConversationBlockRecord.blocked_user_id == user_b),
                (ChatConversationBlockRecord.blocker_id == user_b) & (ChatConversationBlockRecord.blocked_user_id == user_a),
            )
        )
    )
    return row is not None


async def ensure_context(session: AsyncSession, payload: ChatContextRequestCreate) -> None:
    if payload.target_user_id == current_user_id():
        raise error(422, "CHAT_TARGET_INVALID", "Cannot start a context chat with yourself")
    if payload.source_type != "friend" and not payload.source_id:
        raise error(403, "CHAT_CONTEXT_REQUIRED", "A valid interaction source is required")
    if payload.source_type == "friend" and not payload.evidence_id:
        raise error(403, "CHAT_CONTEXT_REQUIRED", "Friend conversations require relationship evidence")
    if await blocked_between(session, current_user_id(), payload.target_user_id):
        raise error(403, "CHAT_BLOCKED", "A block relationship prevents this conversation")


async def create_context_request(session: AsyncSession, payload: ChatContextRequestCreate, commit: bool = True) -> ChatContextRequestOut:
    await ensure_context(session, payload)
    request_id = new_id("ctx")
    audit = record_admin_audit(current_user_id(), "chat_context_request_create", "chat_context_request", request_id)
    row = ChatContextRequestRecord(
        id=request_id,
        initiator_id=current_user_id(),
        target_user_id=payload.target_user_id,
        source_type=payload.source_type,
        source_id=payload.source_id,
        reply_id=payload.reply_id,
        initiator_action=payload.initiator_action,
        evidence_id=payload.evidence_id,
        status="pending",
        audit_refs=audit_refs_dump([audit.id]),
        created_at=now(),
        updated_at=now(),
    )
    session.add(row)
    await session.flush()
    if commit:
        await session.commit()
        await session.refresh(row)
    return to_request_out(row)


async def ensure_seed_invitation(session: AsyncSession) -> None:
    user_id = current_user_id()
    request_id = f"ctx_invite_{user_id}"
    existing = await session.get(ChatContextRequestRecord, request_id)
    if existing is not None:
        return
    inviter_id = SEED_INVITER_ID if user_id != SEED_INVITER_ID else "200000000001"
    audit = record_admin_audit("system", "chat_context_request_seed_invitation", "chat_context_request", request_id)
    session.add(
        ChatContextRequestRecord(
            id=request_id,
            initiator_id=inviter_id,
            target_user_id=user_id,
            source_type="game_room",
            source_id=f"room_invite_{user_id}",
            source_title="游戏房间邀请",
            reply_id=f"message_invite:{user_id}",
            initiator_action="room_confirm",
            evidence_id=f"seed_message_invite:{user_id}",
            status="pending",
            audit_refs=audit_refs_dump([audit.id]),
            created_at=now(),
            updated_at=now(),
        )
    )
    await session.commit()


async def list_context_requests(session: AsyncSession, status: str | None = None) -> list[ChatContextRequestOut]:
    await ensure_seed_invitation(session)
    conditions = [
        or_(
            ChatContextRequestRecord.initiator_id == current_user_id(),
            ChatContextRequestRecord.target_user_id == current_user_id(),
        )
    ]
    if status:
        conditions.append(ChatContextRequestRecord.status == status)
    rows = (await session.execute(select(ChatContextRequestRecord).where(*conditions).order_by(ChatContextRequestRecord.created_at.desc()))).scalars().all()
    rows = sorted(rows, key=lambda item: item.status != "pending")
    return [to_request_out(row) for row in rows]


async def accept_context_request(session: AsyncSession, request_id: str, payload: ChatContextRequestAccept) -> ChatContextRequestOut:
    row = await session.get(ChatContextRequestRecord, request_id)
    if row is None or current_user_id() not in participants(row):
        raise error(404, "CHAT_CONTEXT_REQUEST_NOT_FOUND", "Context request not found")
    if row.status != "pending":
        raise error(409, "CHAT_STATE_CONFLICT", "Context request is not pending")

    conversation_id = new_id("chat")
    audit = record_admin_audit(current_user_id(), "chat_context_request_accept", "chat_conversation", conversation_id)
    refs = audit_refs_load(row.audit_refs)
    refs.append(audit.id)
    conversation = ChatConversationRecord(
        id=conversation_id,
        status="active",
        source_type=row.source_type,
        source_id=row.source_id,
        source_title=row.source_title,
        participant_a_id=row.initiator_id,
        participant_b_id=row.target_user_id,
        friendship_state="friend" if row.source_type == "friend" else "none",
        expires_at=now() + timedelta(days=7),
        risk_state="clear",
        report_state="none",
        audit_refs=audit_refs_dump(refs),
        created_at=now(),
        updated_at=now(),
    )
    session.add(conversation)
    row.status = "active"
    row.conversation_id = conversation_id
    row.confirm_action = payload.confirm_action
    row.confirm_evidence_id = payload.evidence_id
    row.audit_refs = audit_refs_dump(refs)
    row.updated_at = now()
    await session.commit()
    await session.refresh(row)
    return to_request_out(row)


async def reject_context_request(session: AsyncSession, request_id: str, reason: str) -> ChatContextRequestOut:
    row = await session.get(ChatContextRequestRecord, request_id)
    if row is None or current_user_id() not in participants(row):
        raise error(404, "CHAT_CONTEXT_REQUEST_NOT_FOUND", "Context request not found")
    if row.status != "pending":
        raise error(409, "CHAT_STATE_CONFLICT", "Context request is not pending")
    audit = record_admin_audit(current_user_id(), "chat_context_request_reject", "chat_context_request", request_id)
    refs = audit_refs_load(row.audit_refs)
    refs.append(audit.id)
    row.status = "expired"
    row.reject_reason = reason
    row.audit_refs = audit_refs_dump(refs)
    row.updated_at = now()
    await session.commit()
    await session.refresh(row)
    return to_request_out(row)


async def list_conversations(session: AsyncSession, status: str | None = None, source_type: str | None = None) -> list[ChatConversationOut]:
    conditions = [
        or_(
            ChatConversationRecord.participant_a_id == current_user_id(),
            ChatConversationRecord.participant_b_id == current_user_id(),
        )
    ]
    if status:
        conditions.append(ChatConversationRecord.status == status)
    if source_type:
        conditions.append(ChatConversationRecord.source_type == source_type)
    rows = (await session.execute(select(ChatConversationRecord).where(*conditions).order_by(ChatConversationRecord.updated_at.desc()))).scalars().all()
    return [await to_conversation_out(session, row) for row in rows]


async def get_conversation(session: AsyncSession, conversation_id: str) -> ChatConversationOut:
    row = await session.get(ChatConversationRecord, conversation_id)
    if row is None:
        raise error(404, "CHAT_CONVERSATION_NOT_FOUND", "Conversation not found")
    await ensure_participant(row)
    return await to_conversation_out(session, row)


async def send_message(session: AsyncSession, conversation_id: str, payload: ChatMessageCreate) -> ChatMessageSendResponse:
    row = await session.get(ChatConversationRecord, conversation_id)
    if row is None:
        raise error(404, "CHAT_CONVERSATION_NOT_FOUND", "Conversation not found")
    await ensure_participant(row)
    if row.status == "blocked":
        raise error(403, "CHAT_BLOCKED", "Conversation is blocked")
    if row.status != "active":
        raise error(409, "CHAT_CONVERSATION_NOT_ACTIVE", "Conversation is not active")

    labels = [label for word, label in RISK_WORDS.items() if word in payload.content.lower()]
    message_status = "risk_pending" if labels else "sent"
    message_id = payload.client_message_id or new_id("msg")
    session.add(
        ChatMessageRecord(
            id=message_id,
            conversation_id=conversation_id,
            sender_id=current_user_id(),
            content_type=payload.content_type,
            content=payload.content,
            status=message_status,
            created_at=now(),
        )
    )
    row.last_message = payload.content
    row.updated_at = now()
    if labels:
        row.risk_state = "risk_frozen"
        row.status = "risk_frozen"
    audit = record_admin_audit(current_user_id(), "chat_message_send", "chat_conversation", conversation_id)
    refs = audit_refs_load(row.audit_refs)
    refs.append(audit.id)
    row.audit_refs = audit_refs_dump(refs)
    await session.commit()
    return ChatMessageSendResponse(message_id=message_id, status=message_status, risk_labels=labels, audit_id=audit.id)


async def report_conversation(session: AsyncSession, conversation_id: str, payload: ChatConversationReportRequest) -> ChatConversationReportResponse:
    row = await session.get(ChatConversationRecord, conversation_id)
    if row is None:
        raise error(404, "CHAT_CONVERSATION_NOT_FOUND", "Conversation not found")
    await ensure_participant(row)
    report_id = new_id("chat_report")
    audit = record_admin_audit(current_user_id(), "chat_conversation_report", "chat_conversation", conversation_id)
    row.status = "reported"
    row.risk_state = "reported"
    row.report_state = "reported"
    refs = audit_refs_load(row.audit_refs)
    refs.append(audit.id)
    row.audit_refs = audit_refs_dump(refs)
    session.add(
        ChatConversationReportRecord(
            id=report_id,
            conversation_id=conversation_id,
            reporter_id=current_user_id(),
            reason=payload.reason,
            message_ids=json.dumps(payload.message_ids, ensure_ascii=False),
            description=payload.description,
            audit_id=audit.id,
            created_at=now(),
        )
    )
    await session.commit()
    return ChatConversationReportResponse(report_id=report_id, conversation_status="reported", audit_id=audit.id)


async def block_conversation(session: AsyncSession, conversation_id: str, payload: ChatConversationBlockRequest) -> ChatConversationBlockResponse:
    row = await session.get(ChatConversationRecord, conversation_id)
    if row is None:
        raise error(404, "CHAT_CONVERSATION_NOT_FOUND", "Conversation not found")
    await ensure_participant(row)
    if payload.target_user_id not in participants(row) or payload.target_user_id == current_user_id():
        raise error(422, "CHAT_TARGET_INVALID", "Target user is not a valid participant")
    block_id = new_id("chat_block")
    audit = record_admin_audit(current_user_id(), "chat_conversation_block", "chat_conversation", conversation_id)
    row.status = "blocked"
    row.risk_state = "blocked"
    refs = audit_refs_load(row.audit_refs)
    refs.append(audit.id)
    row.audit_refs = audit_refs_dump(refs)
    session.add(
        ChatConversationBlockRecord(
            id=block_id,
            conversation_id=conversation_id,
            blocker_id=current_user_id(),
            blocked_user_id=payload.target_user_id,
            reason=payload.reason,
            audit_id=audit.id,
            created_at=now(),
        )
    )
    await session.commit()
    return ChatConversationBlockResponse(block_id=block_id, conversation_status="blocked", audit_id=audit.id)


async def admin_context_requests(session: AsyncSession) -> list[ChatContextRequestOut]:
    rows = (await session.execute(select(ChatContextRequestRecord).order_by(ChatContextRequestRecord.created_at.desc()))).scalars().all()
    return [to_request_out(row) for row in rows]


async def admin_conversation(session: AsyncSession, conversation_id: str) -> ChatConversationOut:
    row = await session.get(ChatConversationRecord, conversation_id)
    if row is None:
        raise error(404, "CHAT_CONVERSATION_NOT_FOUND", "Conversation not found")
    return await to_conversation_out(session, row)


def to_request_out(row: ChatContextRequestRecord) -> ChatContextRequestOut:
    return ChatContextRequestOut(
        id=row.id,
        status=row.status,
        conversation_id=row.conversation_id,
        source_type=row.source_type,
        source_id=row.source_id,
        source_summary=source_summary(row.source_type, row.source_id, row.source_title),
        rate_limit=rate_limit("friend" if row.source_type == "friend" else "none"),
    )


async def to_conversation_out(session: AsyncSession, row: ChatConversationRecord) -> ChatConversationOut:
    messages = (await session.execute(select(ChatMessageRecord).where(ChatMessageRecord.conversation_id == row.id).order_by(ChatMessageRecord.created_at))).scalars().all()
    return ChatConversationOut(
        id=row.id,
        status=row.status,
        source_type=row.source_type,
        source_id=row.source_id,
        source_summary=source_summary(row.source_type, row.source_id, row.source_title),
        participants=participants(row),
        friendship_state=row.friendship_state,
        expires_at=iso(row.expires_at),
        last_message=row.last_message,
        rate_limit=rate_limit(row.friendship_state),
        risk_state=row.risk_state,
        report_state=row.report_state,
        messages=[
            ChatMessageOut(
                id=message.id,
                sender_id=message.sender_id,
                content_type=message.content_type,
                content=message.content,
                status=message.status,
                created_at=iso(message.created_at) or "",
            )
            for message in messages
        ],
        audit_refs=audit_refs_load(row.audit_refs),
    )
