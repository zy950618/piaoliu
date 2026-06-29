from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.audit import list_admin_audit_logs, record_admin_audit
from app.dependencies import get_current_admin, require_admin_role
from app import db_business
from app.db import get_db_session
from app.schemas import (
    AdminAuditLogOut,
    AdminChatReviewOut,
    AdminContentOut,
    AdminLoginRequest,
    AdminModerationJobOut,
    AdminLogoutResponse,
    AdminPrincipalOut,
    AdminRewardConfig,
    AdminSummary,
    AdminTokenResponse,
    AdminUserStatusRequest,
    AdminUserOut,
    AdminWalletSummary,
    ModerationDecisionRequest,
    NearbyUser,
    PlazaPost,
    ReferralState,
    ReportOut,
    VerificationReviewRequest,
    VerificationState,
)
from app.security import AdminPrincipal, create_mock_admin_token
from app.settings import get_settings

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/auth/login", response_model=AdminTokenResponse)
def admin_login(payload: AdminLoginRequest) -> AdminTokenResponse:
    token = create_mock_admin_token(payload.username, payload.password)
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "ADMIN_LOGIN_FAILED", "message": "Invalid admin credentials"},
        )

    settings = get_settings()
    record_admin_audit(payload.username, "admin_login", "admin_session", payload.username)
    return AdminTokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in=settings.admin_token_expires_seconds,
        admin=AdminPrincipalOut(username=settings.admin_mock_username, roles=["admin", "moderator"]),
    )


@router.post("/auth/logout", response_model=AdminLogoutResponse)
def admin_logout(principal: AdminPrincipal = Depends(get_current_admin)) -> AdminLogoutResponse:
    record_admin_audit(principal.username, "admin_logout", "admin_session", principal.username)
    return AdminLogoutResponse(status="logged_out")


@router.get("/auth/me", response_model=AdminPrincipalOut)
def admin_me(principal: AdminPrincipal = Depends(get_current_admin)) -> AdminPrincipalOut:
    return AdminPrincipalOut(username=principal.username, roles=principal.roles)


@router.get("/reward-config", response_model=AdminRewardConfig)
def admin_reward_config() -> AdminRewardConfig:
    return AdminRewardConfig(
        base_quotas={quota_type: base for quota_type, (_, base) in db_business.BASE_QUOTAS.items()},
        vip_bonus={quota_type: 5 for quota_type in db_business.BASE_QUOTAS},
        ad_cooldown_minutes=15,
        ad_reward_per_quota=10,
        checkin_rewards=db_business.CHECKIN_REWARDS,
        reject_refund_enabled=False,
    )


@router.patch("/reward-config", response_model=AdminRewardConfig)
def update_admin_reward_config(
    payload: AdminRewardConfig,
    principal: AdminPrincipal = Depends(require_admin_role("admin")),
) -> AdminRewardConfig:
    record_admin_audit(principal.username, "update_reward_config", "reward_config", "global")
    return payload


@router.get("/users", response_model=list[AdminUserOut])
async def admin_users(session: AsyncSession = Depends(get_db_session)) -> list[AdminUserOut]:
    rows = await db_business.admin_users(session)
    return [
        AdminUserOut(
            id=user.id,
            nickname=user.nickname,
            avatar_text=user.avatar_text,
            avatar_url=user.avatar_url,
            platform=user.platform if user.platform in {"wechat", "ios", "android", "h5"} else "h5",
            gender=user.gender if user.gender in {"female", "male", "unknown"} else "unknown",
            is_vip=user.is_vip,
            drift_coins=user.drift_coins,
            status=user.status if user.status in {"active", "limited", "blocked"} else "active",
            face_verified=user.face_verified,
            created_at=db_business.iso(user.created_at),
            blocked_until=db_business.iso(restriction.blocked_until) if restriction and restriction.blocked_until else None,
            block_reason=restriction.reason if restriction and restriction.reason else None,
        )
        for user, restriction in rows
    ]


@router.post("/users/{user_id}/status", response_model=AdminUserOut)
async def admin_update_user_status(
    user_id: str,
    payload: AdminUserStatusRequest,
    session: AsyncSession = Depends(get_db_session),
    principal: AdminPrincipal = Depends(require_admin_role("admin", "moderator")),
) -> AdminUserOut:
    user, restriction = await db_business.update_user_status(
        session=session,
        user_id=user_id,
        status=payload.status,
        reason=payload.reason,
        block_days=payload.block_days,
        blocked_until=payload.blocked_until,
    )
    record_admin_audit(principal.username, f"user_status_{payload.status}", "user", user_id)
    return AdminUserOut(
        id=user.id,
        nickname=user.nickname,
        avatar_text=user.avatar_text,
        avatar_url=user.avatar_url,
        platform=user.platform if user.platform in {"wechat", "ios", "android", "h5"} else "h5",
        gender=user.gender if user.gender in {"female", "male", "unknown"} else "unknown",
        is_vip=user.is_vip,
        drift_coins=user.drift_coins,
        status=user.status if user.status in {"active", "limited", "blocked"} else "active",
        face_verified=user.face_verified,
        created_at=db_business.iso(user.created_at),
        blocked_until=db_business.iso(restriction.blocked_until) if restriction and restriction.blocked_until else None,
        block_reason=restriction.reason if restriction and restriction.reason else None,
    )


@router.get("/content", response_model=list[AdminContentOut])
async def admin_content(session: AsyncSession = Depends(get_db_session)) -> list[AdminContentOut]:
    return [
        AdminContentOut(
            id=row_id,
            type=row_type,
            status=status_value,
            author_id=author_id,
            author_name=author_name,
            author_avatar_text=author_avatar_text,
            author_avatar_url=author_avatar_url,
            excerpt=excerpt,
            created_at=db_business.iso(created_at),
        )
        for row_id, row_type, status_value, author_id, author_name, author_avatar_text, author_avatar_url, excerpt, created_at in await db_business.admin_content_rows(session)
    ]


@router.post("/moderation/{job_id}", response_model=AdminModerationJobOut)
def admin_moderation(
    job_id: str,
    payload: ModerationDecisionRequest | None = None,
    principal: AdminPrincipal = Depends(require_admin_role("admin", "moderator")),
) -> AdminModerationJobOut:
    action = payload.action if payload else "approve"
    reason = payload.reason if payload else None
    result = AdminModerationJobOut(
        job_id=job_id,
        status="processed",
        action=action,
        reason=reason,
        audited_at=db_business.iso(db_business.now()),
    )
    record_admin_audit(principal.username, f"moderation_{action}", "moderation_job", job_id)
    return result


@router.get("/summary", response_model=AdminSummary)
async def admin_summary(session: AsyncSession = Depends(get_db_session)) -> AdminSummary:
    counts = await db_business.admin_counts(session)
    return AdminSummary(**counts)


@router.get("/audit", response_model=list[AdminAuditLogOut])
def admin_audit() -> list[AdminAuditLogOut]:
    return list_admin_audit_logs()


@router.get("/wallet", response_model=AdminWalletSummary)
async def admin_wallet(session: AsyncSession = Depends(get_db_session)) -> AdminWalletSummary:
    wallet = await db_business.wallet_state(session)
    return AdminWalletSummary(
        recharge_coins=wallet.recharge_coins,
        earned_coins=wallet.earned_coins,
        gift_coins=wallet.gift_coins,
        frozen_coins=wallet.frozen_coins,
        pending_withdrawals=1 if wallet.frozen_coins > 0 else 0,
    )


@router.get("/verification", response_model=VerificationState)
async def admin_verification(session: AsyncSession = Depends(get_db_session)) -> VerificationState:
    verification, _ = await db_business.verification_overview(session)
    return verification


@router.post("/verification/{user_id}/review", response_model=VerificationState)
async def admin_review_verification(
    user_id: str,
    payload: VerificationReviewRequest,
    session: AsyncSession = Depends(get_db_session),
    principal: AdminPrincipal = Depends(require_admin_role("admin", "moderator")),
) -> VerificationState:
    return await db_business.review_verification(session, user_id, payload.action, payload.reason or principal.username)


@router.get("/reports", response_model=list[ReportOut])
async def admin_reports(session: AsyncSession = Depends(get_db_session)) -> list[ReportOut]:
    return await db_business.list_reports(session)


@router.get("/chats", response_model=list[AdminChatReviewOut])
async def admin_chats(session: AsyncSession = Depends(get_db_session)) -> list[AdminChatReviewOut]:
    return await db_business.admin_chat_reviews(session)


@router.get("/referral", response_model=ReferralState)
async def admin_referral(session: AsyncSession = Depends(get_db_session)) -> ReferralState:
    _, referral = await db_business.verification_overview(session)
    return referral


@router.get("/nearby", response_model=list[NearbyUser])
async def admin_nearby(session: AsyncSession = Depends(get_db_session)) -> list[NearbyUser]:
    return await db_business.list_nearby(session)


@router.get("/plaza", response_model=list[PlazaPost])
async def admin_plaza(session: AsyncSession = Depends(get_db_session)) -> list[PlazaPost]:
    return await db_business.list_plaza(session)
