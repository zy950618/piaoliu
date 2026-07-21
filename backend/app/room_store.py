import json
import secrets
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import db_business
from app.models import ChatConversationRecord, ConversationThread, GameRound, Room, RoomInvitation, RoomMember
from app.schemas import (
    GameRoundCreate,
    GameRoundOut,
    RoomCreate,
    RoomInvitationCreate,
    RoomInvitationOut,
    RoomMemberOut,
    RoomOut,
)


def now() -> datetime:
    return datetime.now(UTC)


def is_expired(value: datetime) -> bool:
    comparable = value if value.tzinfo is not None else value.replace(tzinfo=UTC)
    return comparable <= now()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex}"


def error(status: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status, detail={"code": code, "message": message})


async def require_room(session: AsyncSession, room_id: str) -> Room:
    room = await session.get(Room, room_id)
    if room is None:
        raise error(404, "ROOM_NOT_FOUND", "房间不存在或已被移除")
    return room


async def active_member(session: AsyncSession, room_id: str, user_id: str | None = None) -> RoomMember | None:
    return await session.scalar(
        select(RoomMember).where(
            RoomMember.room_id == room_id,
            RoomMember.user_id == (user_id or db_business.current_user_id()),
            RoomMember.status == "active",
        )
    )


async def require_active_member(session: AsyncSession, room_id: str) -> RoomMember:
    member = await active_member(session, room_id)
    if member is None:
        raise error(403, "ROOM_MEMBERSHIP_REQUIRED", "加入房间后才能执行此操作")
    return member


async def room_out(session: AsyncSession, room: Room) -> RoomOut:
    members = (
        await session.execute(select(RoomMember).where(RoomMember.room_id == room.id).order_by(RoomMember.joined_at))
    ).scalars().all()
    return RoomOut(
        id=room.id,
        owner_id=room.owner_id,
        conversation_id=room.conversation_id,
        name=room.name,
        visibility=room.visibility,
        size_mode=room.size_mode,
        join_policy=room.join_policy,
        capacity=room.capacity,
        allow_member_invite=room.allow_member_invite,
        status=room.status,
        members=[RoomMemberOut(user_id=item.user_id, role=item.role, status=item.status) for item in members],
        created_at=room.created_at.isoformat(),
    )


async def create_room(session: AsyncSession, payload: RoomCreate) -> RoomOut:
    user = await db_business.get_current_user(session)
    if payload.size_mode == "pair" and payload.capacity != 2:
        raise error(422, "ROOM_CAPACITY_INVALID", "双人房容量必须为 2 人")
    if payload.visibility == "private":
        if not payload.conversation_id:
            raise error(422, "ROOM_CONVERSATION_REQUIRED", "私密房必须从有效聊天中创建")
        conversation = await session.get(ChatConversationRecord, payload.conversation_id)
        legacy_conversation = await session.get(ConversationThread, payload.conversation_id) if conversation is None else None
        participants = (
            {conversation.participant_a_id, conversation.participant_b_id}
            if conversation is not None
            else {legacy_conversation.user_a_id, legacy_conversation.user_b_id}
            if legacy_conversation is not None
            else set()
        )
        if user.id not in participants:
            raise error(403, "ROOM_CONVERSATION_INVALID", "当前聊天不能用于创建私密房")
        if payload.join_policy != "invite":
            raise error(422, "ROOM_JOIN_POLICY_INVALID", "私密房仅支持邀请加入")
    room = Room(
        id=new_id("room"),
        owner_id=user.id,
        conversation_id=payload.conversation_id,
        name=payload.name,
        visibility=payload.visibility,
        size_mode=payload.size_mode,
        join_policy=payload.join_policy,
        capacity=payload.capacity,
        allow_member_invite=payload.allow_member_invite,
        status="active",
        last_active_at=now(),
        created_at=now(),
    )
    session.add(room)
    session.add(
        RoomMember(
            id=new_id("member"),
            room_id=room.id,
            user_id=user.id,
            role="owner",
            status="active",
            joined_at=now(),
        )
    )
    await session.commit()
    await session.refresh(room)
    return await room_out(session, room)


async def list_rooms(session: AsyncSession, scope: str) -> list[RoomOut]:
    user = await db_business.get_current_user(session)
    if scope == "public":
        rows = (
            await session.execute(
                select(Room).where(Room.visibility == "public", Room.status == "active").order_by(Room.last_active_at.desc())
            )
        ).scalars().all()
    else:
        member_room_ids = select(RoomMember.room_id).where(RoomMember.user_id == user.id, RoomMember.status == "active")
        rows = (
            await session.execute(select(Room).where(Room.id.in_(member_room_ids)).order_by(Room.last_active_at.desc()))
        ).scalars().all()
    return [await room_out(session, row) for row in rows]


async def get_room(session: AsyncSession, room_id: str) -> RoomOut:
    room = await require_room(session, room_id)
    if room.visibility != "public" and await active_member(session, room_id) is None:
        raise error(403, "ROOM_MEMBERSHIP_REQUIRED", "加入房间后才能查看房间详情")
    return await room_out(session, room)


async def create_invitation(session: AsyncSession, room_id: str, payload: RoomInvitationCreate) -> RoomInvitationOut:
    room = await require_room(session, room_id)
    actor = await require_active_member(session, room_id)
    if actor.role not in {"owner", "moderator"} and not room.allow_member_invite:
        raise error(403, "ROOM_INVITE_FORBIDDEN", "当前房间仅房主或管理员可以邀请成员")
    if await active_member(session, room_id, payload.invitee_id):
        raise error(409, "ROOM_MEMBER_EXISTS", "对方已经在房间中")
    existing = await session.scalar(
        select(RoomInvitation).where(
            RoomInvitation.inviter_id == actor.user_id,
            RoomInvitation.idempotency_key == payload.idempotency_key,
        )
    )
    if existing is None:
        existing = RoomInvitation(
            id=new_id("invite"),
            room_id=room_id,
            inviter_id=actor.user_id,
            invitee_id=payload.invitee_id,
            status="pending",
            idempotency_key=payload.idempotency_key,
            expires_at=now() + timedelta(hours=24),
            created_at=now(),
            updated_at=now(),
        )
        session.add(existing)
        await session.commit()
        await session.refresh(existing)
        await db_business.add_user_notification(
            session,
            payload.invitee_id,
            "收到房间邀请",
            f"有人邀请你加入“{room.name}”，邀请将在 24 小时后失效。",
            "room_invitation",
            existing.id,
        )
        await session.commit()
    return invitation_out(existing)


async def list_invitations(session: AsyncSession, status: str = "pending") -> list[RoomInvitationOut]:
    user = await db_business.get_current_user(session)
    rows = (
        await session.execute(
            select(RoomInvitation)
            .where(RoomInvitation.invitee_id == user.id, RoomInvitation.status == status)
            .order_by(RoomInvitation.created_at.desc())
        )
    ).scalars().all()
    return [invitation_out(row) for row in rows]


def invitation_out(row: RoomInvitation) -> RoomInvitationOut:
    return RoomInvitationOut(
        id=row.id,
        room_id=row.room_id,
        inviter_id=row.inviter_id,
        invitee_id=row.invitee_id,
        status=row.status,
        expires_at=row.expires_at.isoformat(),
    )


async def accept_invitation(session: AsyncSession, invitation_id: str) -> RoomOut:
    user = await db_business.get_current_user(session)
    invitation = await session.get(RoomInvitation, invitation_id)
    if invitation is None or invitation.invitee_id != user.id:
        raise error(404, "ROOM_INVITATION_NOT_FOUND", "邀请不存在或不属于当前用户")
    if invitation.status != "pending" or is_expired(invitation.expires_at):
        raise error(409, "ROOM_INVITATION_INACTIVE", "邀请已处理或已过期")
    room = await require_room(session, invitation.room_id)
    if room.status != "active":
        raise error(409, "ROOM_NOT_ACTIVE", "房间已经结束")
    member_count = len(
        (await session.execute(select(RoomMember.id).where(RoomMember.room_id == room.id, RoomMember.status == "active"))).all()
    )
    if member_count >= room.capacity:
        raise error(409, "ROOM_FULL", "房间人数已满")
    member = await session.scalar(
        select(RoomMember).where(RoomMember.room_id == room.id, RoomMember.user_id == user.id)
    )
    if member is None:
        session.add(
            RoomMember(
                id=new_id("member"), room_id=room.id, user_id=user.id, role="member", status="active", joined_at=now()
            )
        )
    else:
        if member.cannot_rejoin:
            raise error(403, "ROOM_REJOIN_FORBIDDEN", "你已被移出该房间，不能再次加入")
        member.status = "active"
        member.left_at = None
        member.joined_at = now()
    invitation.status = "accepted"
    invitation.updated_at = now()
    room.last_active_at = now()
    await session.commit()
    return await room_out(session, room)


async def join_public_room(session: AsyncSession, room_id: str) -> RoomOut:
    user = await db_business.get_current_user(session)
    room = await require_room(session, room_id)
    if room.visibility != "public" or room.join_policy != "open" or room.status != "active":
        raise error(403, "ROOM_JOIN_FORBIDDEN", "该房间当前不支持直接加入")
    existing = await active_member(session, room_id, user.id)
    if existing is not None:
        return await room_out(session, room)
    member_count = len(
        (await session.execute(select(RoomMember.id).where(RoomMember.room_id == room.id, RoomMember.status == "active"))).all()
    )
    if member_count >= room.capacity:
        raise error(409, "ROOM_FULL", "房间人数已满")
    session.add(RoomMember(id=new_id("member"), room_id=room.id, user_id=user.id, role="member", status="active", joined_at=now()))
    room.last_active_at = now()
    await session.commit()
    return await room_out(session, room)


async def dissolve_room(session: AsyncSession, room_id: str) -> RoomOut:
    room = await require_room(session, room_id)
    if room.owner_id != db_business.current_user_id():
        raise error(403, "ROOM_OWNER_REQUIRED", "只有房主可以结束房间")
    if room.status == "active":
        room.status = "ended"
        room.dissolved_at = now()
        await session.commit()
    return await room_out(session, room)


async def create_game_round(session: AsyncSession, room_id: str, payload: GameRoundCreate) -> GameRoundOut:
    room = await require_room(session, room_id)
    member = await require_active_member(session, room_id)
    if room.status != "active":
        raise error(409, "ROOM_NOT_ACTIVE", "房间已经结束")
    prompt_id = None
    prompt_text = None
    result: dict
    if payload.mode == "dice":
        result = {"value": secrets.randbelow(6) + 1, "sides": 6}
    else:
        prompt_mode = f"{payload.mode}_{'private' if room.visibility == 'private' else 'public'}"
        prompt = await db_business.random_game_prompt(session, prompt_mode)
        prompt_id = prompt.id
        prompt_text = prompt.text
        result = {"visibility": prompt.visibility, "meaning": prompt.meaning}
    timestamp = now()
    row = GameRound(
        id=new_id("round"),
        room_id=room_id,
        initiator_id=member.user_id,
        mode=payload.mode,
        status="resolved",
        prompt_id=prompt_id,
        prompt_text=prompt_text,
        result_json=json.dumps(result, ensure_ascii=False),
        created_at=timestamp,
        resolved_at=timestamp,
    )
    session.add(row)
    room.last_active_at = timestamp
    await session.commit()
    await session.refresh(row)
    return game_round_out(row)


def game_round_out(row: GameRound) -> GameRoundOut:
    return GameRoundOut(
        id=row.id,
        room_id=row.room_id,
        initiator_id=row.initiator_id,
        mode=row.mode,
        status=row.status,
        prompt_id=row.prompt_id,
        prompt_text=row.prompt_text,
        result=json.loads(row.result_json),
        created_at=row.created_at.isoformat(),
        resolved_at=row.resolved_at.isoformat() if row.resolved_at else None,
    )
