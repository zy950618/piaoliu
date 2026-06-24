from fastapi import APIRouter, Depends, HTTPException, status

from app.audit import list_admin_audit_logs, record_admin_audit
from app.dependencies import get_current_admin, require_admin_role
from app import mock_store
from app.mock_store import get_reward_config, iso_now
from app.routes import wallet as wallet_routes
from app.schemas import (
    AdminAuditLogOut,
    AdminContentOut,
    AdminLoginRequest,
    AdminModerationJobOut,
    AdminLogoutResponse,
    AdminPrincipalOut,
    AdminRewardConfig,
    AdminSummary,
    AdminTokenResponse,
    AdminUserOut,
    AdminWalletSummary,
    ModerationDecisionRequest,
    NearbyUser,
    PlazaPost,
    ReferralState,
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
    return get_reward_config()


@router.patch("/reward-config", response_model=AdminRewardConfig)
def update_admin_reward_config(
    payload: AdminRewardConfig,
    principal: AdminPrincipal = Depends(require_admin_role("admin")),
) -> AdminRewardConfig:
    record_admin_audit(principal.username, "update_reward_config", "reward_config", "global")
    return payload


@router.get("/users", response_model=list[AdminUserOut])
def admin_users() -> list[AdminUserOut]:
    return [
        AdminUserOut(
            id=mock_store.user.id,
            nickname=mock_store.user.nickname,
            is_vip=mock_store.user.is_vip,
            drift_coins=mock_store.user.drift_coins,
            status="active",
            face_verified=mock_store.user.face_verified,
            created_at=iso_now(),
        ),
        AdminUserOut(
            id="user_mock_002",
            nickname="Mock Visitor",
            is_vip=False,
            drift_coins=80,
            status="limited",
            face_verified=False,
            created_at=iso_now(),
        ),
    ]


@router.get("/content", response_model=list[AdminContentOut])
def admin_content() -> list[AdminContentOut]:
    bottle_items = [
        AdminContentOut(
            id=item.id,
            type="bottle",
            status=item.status,
            author_id=item.author_id,
            excerpt=item.content[:60],
            created_at=item.created_at,
        )
        for item in mock_store.bottles
    ]
    treehole_items = [
        AdminContentOut(
            id=item.id,
            type="treehole",
            status=item.status,
            author_id=item.author_id,
            excerpt=item.content[:60],
            created_at=item.created_at,
        )
        for item in mock_store.treeholes
    ]
    return bottle_items + treehole_items


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
        audited_at=iso_now(),
    )
    record_admin_audit(principal.username, f"moderation_{action}", "moderation_job", job_id)
    return result


@router.get("/summary", response_model=AdminSummary)
def admin_summary() -> AdminSummary:
    return AdminSummary(users=12840, pending_content=36, reports=12, ad_rewards_today=2180, orders_today=94)


@router.get("/audit", response_model=list[AdminAuditLogOut])
def admin_audit() -> list[AdminAuditLogOut]:
    return list_admin_audit_logs()


@router.get("/wallet", response_model=AdminWalletSummary)
def admin_wallet() -> AdminWalletSummary:
    wallet = wallet_routes.wallet
    return AdminWalletSummary(
        recharge_coins=wallet.recharge_coins,
        earned_coins=wallet.earned_coins,
        gift_coins=wallet.gift_coins,
        frozen_coins=wallet.frozen_coins,
        pending_withdrawals=1 if wallet.frozen_coins > 0 else 0,
    )


@router.get("/verification", response_model=VerificationState)
def admin_verification() -> VerificationState:
    return wallet_routes.verification


@router.get("/referral", response_model=ReferralState)
def admin_referral() -> ReferralState:
    return wallet_routes.referral


@router.get("/nearby", response_model=list[NearbyUser])
def admin_nearby() -> list[NearbyUser]:
    return wallet_routes.nearby_users


@router.get("/plaza", response_model=list[PlazaPost])
def admin_plaza() -> list[PlazaPost]:
    return wallet_routes.plaza_posts
