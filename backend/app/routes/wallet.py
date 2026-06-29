from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import db_business
from app.db import get_db_session
from app.schemas import (
    BlacklistItem,
    CreatorProfile,
    GiftSendResponse,
    PhotoUnlockResponse,
    PrivatePhoto,
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


@router.get("/private-photos", response_model=list[PrivatePhoto])
async def list_private_photos(session: AsyncSession = Depends(get_db_session)) -> list[PrivatePhoto]:
    return await db_business.list_private_photos(session)


@router.post("/private-photos/unlock", response_model=PhotoUnlockResponse)
async def unlock_private_photo(payload: UnlockPhotoRequest, session: AsyncSession = Depends(get_db_session)) -> PhotoUnlockResponse:
    return await db_business.unlock_private_photo(session, payload.photo_id)


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
