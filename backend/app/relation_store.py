from datetime import UTC, datetime
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import db_business
from app.models import BlacklistEntry, ChatGrant, FriendRequest, Friendship, User
from app.schemas import FriendRequestOut, FriendshipOut, RelationStateOut


def now() -> datetime:
    return datetime.now(UTC)


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex}"


def error(status: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status, detail={"code": code, "message": message})


def ordered_pair(user_a: str, user_b: str) -> tuple[str, str]:
    return tuple(sorted((user_a, user_b)))


async def blocked_between(session: AsyncSession, user_a: str, user_b: str) -> bool:
    row = await session.scalar(
        select(BlacklistEntry).where(
            BlacklistEntry.status == "blocked",
            or_(
                (BlacklistEntry.owner_id == user_a) & (BlacklistEntry.blocked_user_id == user_b),
                (BlacklistEntry.owner_id == user_b) & (BlacklistEntry.blocked_user_id == user_a),
            ),
        )
    )
    return row is not None


async def create_friend_request(session: AsyncSession, target_user_id: str) -> FriendRequestOut:
    user = await db_business.get_current_user(session)
    if target_user_id == user.id:
        raise error(422, "FRIEND_TARGET_INVALID", "不能向自己发送好友申请")
    target = await session.get(User, target_user_id)
    if target is None:
        raise error(404, "USER_NOT_FOUND", "用户不存在")
    if await blocked_between(session, user.id, target_user_id):
        raise error(403, "RELATION_BLOCKED", "拉黑关系存在，无法发送好友申请")
    pair = ordered_pair(user.id, target_user_id)
    friendship = await session.scalar(
        select(Friendship).where(Friendship.user_a_id == pair[0], Friendship.user_b_id == pair[1], Friendship.status == "active")
    )
    if friendship is not None:
        raise error(409, "FRIENDSHIP_EXISTS", "你们已经是好友")
    row = await session.scalar(
        select(FriendRequest).where(FriendRequest.requester_id == user.id, FriendRequest.target_user_id == target_user_id)
    )
    should_notify = False
    if row is None:
        row = FriendRequest(
            id=new_id("friend"), requester_id=user.id, target_user_id=target_user_id, status="requested", created_at=now()
        )
        session.add(row)
        should_notify = True
    elif row.status in {"rejected", "cancelled"}:
        row.status = "requested"
        row.created_at = now()
        should_notify = True
    if should_notify:
        await db_business.add_notification(
            session,
            "好友申请已发送",
            "好友用于长期关系沉淀；明确互动上下文内仍可按规则继续聊。",
            "friend",
            target_user_id,
        )
    await session.commit()
    await session.refresh(row)
    return request_out(row)


async def list_friend_requests(session: AsyncSession, direction: str) -> list[FriendRequestOut]:
    user = await db_business.get_current_user(session)
    condition = FriendRequest.target_user_id == user.id if direction == "incoming" else FriendRequest.requester_id == user.id
    rows = (await session.execute(select(FriendRequest).where(condition).order_by(FriendRequest.created_at.desc()))).scalars().all()
    return [request_out(row) for row in rows]


async def resolve_friend_request(session: AsyncSession, request_id: str, accept: bool) -> FriendRequestOut:
    user = await db_business.get_current_user(session)
    row = await session.get(FriendRequest, request_id)
    if row is None or row.target_user_id != user.id:
        raise error(404, "FRIEND_REQUEST_NOT_FOUND", "好友申请不存在或不属于当前用户")
    if row.status != "requested":
        raise error(409, "FRIEND_REQUEST_INACTIVE", "好友申请已经处理")
    if await blocked_between(session, row.requester_id, row.target_user_id):
        raise error(403, "RELATION_BLOCKED", "拉黑关系存在，无法接受好友申请")
    row.status = "accepted" if accept else "rejected"
    if accept:
        pair = ordered_pair(row.requester_id, row.target_user_id)
        friendship = await session.scalar(
            select(Friendship).where(Friendship.user_a_id == pair[0], Friendship.user_b_id == pair[1])
        )
        if friendship is None:
            friendship = Friendship(
                id=new_id("friendship"), user_a_id=pair[0], user_b_id=pair[1], status="active", created_at=now()
            )
            session.add(friendship)
        else:
            friendship.status = "active"
            friendship.removed_at = None
        grant = await session.scalar(
            select(ChatGrant).where(
                ChatGrant.user_a_id == pair[0],
                ChatGrant.user_b_id == pair[1],
                ChatGrant.source_type == "friend",
                ChatGrant.source_id == friendship.id,
            )
        )
        if grant is None:
            session.add(
                ChatGrant(
                    id=new_id("grant"),
                    user_a_id=pair[0],
                    user_b_id=pair[1],
                    source_type="friend",
                    source_id=friendship.id,
                    status="active",
                    created_at=now(),
                )
            )
        else:
            grant.status = "active"
            grant.revoked_at = None
    await session.commit()
    await session.refresh(row)
    return request_out(row)


async def list_friends(session: AsyncSession) -> list[FriendshipOut]:
    user = await db_business.get_current_user(session)
    rows = (
        await session.execute(
            select(Friendship).where(
                Friendship.status == "active",
                or_(Friendship.user_a_id == user.id, Friendship.user_b_id == user.id),
            )
        )
    ).scalars().all()
    return [friendship_out(row, user.id) for row in rows]


async def remove_friend(session: AsyncSession, target_user_id: str) -> FriendshipOut:
    user = await db_business.get_current_user(session)
    pair = ordered_pair(user.id, target_user_id)
    row = await session.scalar(
        select(Friendship).where(Friendship.user_a_id == pair[0], Friendship.user_b_id == pair[1], Friendship.status == "active")
    )
    if row is None:
        raise error(404, "FRIENDSHIP_NOT_FOUND", "好友关系不存在")
    row.status = "removed"
    row.removed_at = now()
    grants = (
        await session.execute(
            select(ChatGrant).where(ChatGrant.user_a_id == pair[0], ChatGrant.user_b_id == pair[1], ChatGrant.status == "active")
        )
    ).scalars().all()
    for grant in grants:
        grant.status = "revoked"
        grant.revoked_at = now()
    await session.commit()
    return friendship_out(row, user.id)


async def relation_state(session: AsyncSession, target_user_id: str) -> RelationStateOut:
    user = await db_business.get_current_user(session)
    if await blocked_between(session, user.id, target_user_id):
        return RelationStateOut(target_user_id=target_user_id, state="blocked", can_chat=False, can_request_friend=False)
    pair = ordered_pair(user.id, target_user_id)
    friendship = await session.scalar(
        select(Friendship).where(Friendship.user_a_id == pair[0], Friendship.user_b_id == pair[1], Friendship.status == "active")
    )
    if friendship is not None:
        return RelationStateOut(target_user_id=target_user_id, state="friend", can_chat=True, can_request_friend=False)
    request = await session.scalar(
        select(FriendRequest).where(
            FriendRequest.status == "requested",
            or_(
                (FriendRequest.requester_id == user.id) & (FriendRequest.target_user_id == target_user_id),
                (FriendRequest.requester_id == target_user_id) & (FriendRequest.target_user_id == user.id),
            ),
        )
    )
    if request is not None:
        state = "pending_outgoing" if request.requester_id == user.id else "pending_incoming"
        return RelationStateOut(target_user_id=target_user_id, state=state, can_chat=False, can_request_friend=False)
    grant = await session.scalar(
        select(ChatGrant).where(
            ChatGrant.user_a_id == pair[0], ChatGrant.user_b_id == pair[1], ChatGrant.status == "active"
        )
    )
    return RelationStateOut(
        target_user_id=target_user_id,
        state="stranger",
        can_chat=grant is not None,
        can_request_friend=True,
    )


def request_out(row: FriendRequest) -> FriendRequestOut:
    return FriendRequestOut(
        id=row.id,
        requester_id=row.requester_id,
        target_user_id=row.target_user_id,
        status=row.status,
        created_at=row.created_at.isoformat(),
    )


def friendship_out(row: Friendship, user_id: str) -> FriendshipOut:
    friend_id = row.user_b_id if row.user_a_id == user_id else row.user_a_id
    return FriendshipOut(
        id=row.id,
        user_id=user_id,
        friend_user_id=friend_id,
        status=row.status,
        created_at=row.created_at.isoformat(),
    )
