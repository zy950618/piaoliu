from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import db_business, private_photo_review_store
from app.db import get_db_session
from app.dependencies import require_admin_role
from app.schemas import (
    AdminPrivatePhotoReviewOut,
    AdminPrivatePhotoReviewRequest,
    AdminPrivatePhotoReviewResponse,
    AdminPrivatePhotoRiskSummary,
    BlacklistItem,
    CreatorProfile,
    GiftSendResponse,
    PhotoUnlockResponse,
    PrivatePhotoAppealRequest,
    PrivatePhotoAppealResponse,
    PrivatePhotoCreateRequest,
    PrivatePhoto,
    PrivatePhotoReviewOut,
    PrivatePhotoUnlockNewResponse,
    ReferralClaimResponse,
    SendGiftRequest,
    UnlockPhotoRequest,
    VerificationOverview,
    VerificationState,
    WalletOverview,
    WalletRechargeRequest,
    WalletRechargeResponse,
    WithdrawRequest,
    WithdrawResponse,
)
from app.security import AdminPrincipal

router = APIRouter(tags=["wallet"])


@router.get("/wallet", response_model=WalletOverview)
async def get_wallet(session: AsyncSession = Depends(get_db_session)) -> WalletOverview:
    wallet, ledger, gifts = await db_business.wallet_overview(session)
    return WalletOverview(wallet=wallet, ledger=ledger, gifts=gifts)


@router.post("/wallet/recharge", response_model=WalletRechargeResponse)
async def recharge_wallet(payload: WalletRechargeRequest, session: AsyncSession = Depends(get_db_session)) -> WalletRechargeResponse:
    order_id, wallet = await db_business.recharge_wallet(session, payload.amount, payload.channel)
    return WalletRechargeResponse(order_id=order_id, wallet=wallet)


@router.get("/creators", response_model=list[CreatorProfile])
async def list_creators(session: AsyncSession = Depends(get_db_session)) -> list[CreatorProfile]:
    return await db_business.list_creators(session)


@router.get("/verification", response_model=VerificationOverview)
async def get_verification(session: AsyncSession = Depends(get_db_session)) -> VerificationOverview:
    verification, referral = await db_business.verification_overview(session)
    return VerificationOverview(verification=verification, referral=referral)


@router.post("/verification/face", response_model=VerificationState)
async def submit_face_verification(session: AsyncSession = Depends(get_db_session)) -> VerificationState:
    return await db_business.submit_verification(session)


@router.post("/referrals/claim-vip", response_model=ReferralClaimResponse)
async def claim_referral_vip(session: AsyncSession = Depends(get_db_session)) -> ReferralClaimResponse:
    _, referral = await db_business.verification_overview(session)
    return ReferralClaimResponse(status="not_enough", referral=referral)


@router.get("/blacklist", response_model=list[BlacklistItem])
async def list_blacklist(session: AsyncSession = Depends(get_db_session)) -> list[BlacklistItem]:
    return await db_business.list_blacklist(session)


@router.post("/private-photos", response_model=PrivatePhotoReviewOut)
async def create_private_photo(
    payload: PrivatePhotoCreateRequest,
    session: AsyncSession = Depends(get_db_session),
) -> PrivatePhotoReviewOut:
    return await private_photo_review_store.create_photo(session, payload)


@router.get("/private-photos")
async def list_private_photos(
    review_status: str | None = None,
    risk_level: str | None = None,
    session: AsyncSession = Depends(get_db_session),
):
    if review_status or risk_level:
        return await private_photo_review_store.list_photos(session, review_status=review_status, risk_level=risk_level)
    return await db_business.list_private_photos(session)


@router.post("/private-photos/unlock", response_model=PhotoUnlockResponse)
async def unlock_private_photo(payload: UnlockPhotoRequest, session: AsyncSession = Depends(get_db_session)) -> PhotoUnlockResponse:
    return await db_business.unlock_private_photo(session, payload.photo_id)


@router.get("/private-photos/{photo_id}", response_model=PrivatePhotoReviewOut)
async def get_private_photo(
    photo_id: str,
    session: AsyncSession = Depends(get_db_session),
) -> PrivatePhotoReviewOut:
    return await private_photo_review_store.get_photo(session, photo_id)


@router.post("/private-photos/{photo_id}/unlock", response_model=PrivatePhotoUnlockNewResponse)
async def unlock_reviewed_private_photo(
    photo_id: str,
    session: AsyncSession = Depends(get_db_session),
) -> PrivatePhotoUnlockNewResponse:
    return await private_photo_review_store.unlock_photo(session, photo_id)


@router.post("/private-photos/{photo_id}/appeal", response_model=PrivatePhotoAppealResponse)
async def appeal_private_photo(
    photo_id: str,
    payload: PrivatePhotoAppealRequest,
    session: AsyncSession = Depends(get_db_session),
) -> PrivatePhotoAppealResponse:
    return await private_photo_review_store.appeal_photo(session, photo_id, payload)


@router.get("/admin/private-photos/reviews", response_model=list[AdminPrivatePhotoReviewOut])
async def admin_private_photo_reviews(
    review_status: str | None = None,
    risk_level: str | None = None,
    user_id: str | None = None,
    _: AdminPrincipal = Depends(require_admin_role("admin", "moderator")),
    session: AsyncSession = Depends(get_db_session),
) -> list[AdminPrivatePhotoReviewOut]:
    return await private_photo_review_store.admin_reviews(session, review_status=review_status, risk_level=risk_level, user_id=user_id)


@router.get("/admin/private-photos/reviews/{review_id}", response_model=AdminPrivatePhotoReviewOut)
async def admin_private_photo_review_detail(
    review_id: str,
    _: AdminPrincipal = Depends(require_admin_role("admin", "moderator")),
    session: AsyncSession = Depends(get_db_session),
) -> AdminPrivatePhotoReviewOut:
    return await private_photo_review_store.admin_review_detail(session, review_id)


@router.post("/admin/private-photos/reviews/{review_id}/review", response_model=AdminPrivatePhotoReviewResponse)
async def admin_review_private_photo(
    review_id: str,
    payload: AdminPrivatePhotoReviewRequest,
    _: AdminPrincipal = Depends(require_admin_role("admin", "moderator")),
    session: AsyncSession = Depends(get_db_session),
) -> AdminPrivatePhotoReviewResponse:
    return await private_photo_review_store.apply_admin_review(session, review_id, payload)


@router.get("/admin/private-photos/risk-summary", response_model=AdminPrivatePhotoRiskSummary)
async def admin_private_photo_risk_summary(
    _: AdminPrincipal = Depends(require_admin_role("admin", "moderator")),
    session: AsyncSession = Depends(get_db_session),
) -> AdminPrivatePhotoRiskSummary:
    return await private_photo_review_store.risk_summary(session)


@router.post("/gifts/send", response_model=GiftSendResponse)
async def send_gift(payload: SendGiftRequest, session: AsyncSession = Depends(get_db_session)) -> GiftSendResponse:
    wallet = await db_business.send_gift(session, payload.gift_id, payload.receiver_id, "plaza", payload.receiver_id)
    return GiftSendResponse(status="sent", receiver_id=payload.receiver_id, wallet=wallet)


@router.post("/wallet/withdraw", response_model=WithdrawResponse)
async def request_withdraw(payload: WithdrawRequest, session: AsyncSession = Depends(get_db_session)) -> WithdrawResponse:
    wallet = await db_business.wallet_state(session)
    if wallet.charm_value < wallet.withdraw_threshold_charm or payload.amount * wallet.charm_exchange_rate > wallet.charm_value:
        from fastapi import HTTPException

        raise HTTPException(status_code=409, detail="CHARM_LIMIT")
    # The commercial path would create a withdrawal review order. For now the money is frozen in DB via wallet mutation.
    account = await session.get(db_business.WalletAccount, db_business.current_user_id())
    account.withdrawable_coins -= payload.amount
    account.frozen_coins += payload.amount
    account.charm_value -= payload.amount * account.charm_exchange_rate
    await session.commit()
    return WithdrawResponse(status="reviewing", wallet=await db_business.wallet_state(session))
