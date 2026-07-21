from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import db_business
from app.db import get_db_session
from app.payment_verification import issue_mock_payment_receipt, mock_payments_enabled, verify_payment_receipt
from app.schemas import (
    MembershipOrderOut,
    MembershipProduct,
    MockPaymentSession,
    MockPaymentSessionRequest,
    OrderVerifyRequest,
    OrderVerifyResponse,
    PaymentCapability,
)

router = APIRouter(tags=["membership"])


@router.get("/membership/products", response_model=list[MembershipProduct])
async def membership_products(session: AsyncSession = Depends(get_db_session)) -> list[MembershipProduct]:
    return await db_business.list_membership_products(session)


@router.get("/orders", response_model=list[MembershipOrderOut])
async def list_orders(session: AsyncSession = Depends(get_db_session)) -> list[MembershipOrderOut]:
    return await db_business.list_membership_orders(session)


@router.get("/membership/orders", response_model=list[MembershipOrderOut])
async def list_membership_orders(session: AsyncSession = Depends(get_db_session)) -> list[MembershipOrderOut]:
    return await db_business.list_membership_orders(session)


@router.get("/membership/payment-capability", response_model=PaymentCapability)
async def payment_capability() -> PaymentCapability:
    if mock_payments_enabled():
        return PaymentCapability(
            mode="mock",
            can_purchase=True,
            message="开发环境由服务端签发并验证模拟支付凭证，不会产生真实扣款。",
        )
    return PaymentCapability(
        mode="unavailable",
        can_purchase=False,
        message="支付服务尚未配置，请稍后再试。",
    )


@router.post("/membership/mock-payment/session", response_model=MockPaymentSession)
async def create_mock_payment_session(
    payload: MockPaymentSessionRequest,
    session: AsyncSession = Depends(get_db_session),
) -> MockPaymentSession:
    user = await db_business.get_current_user(session)
    await db_business.ensure_membership_product_available(session, payload.platform, payload.product_id)
    issued = issue_mock_payment_receipt(user_id=user.id, platform=payload.platform, product_id=payload.product_id)
    return MockPaymentSession(
        transaction_id=issued.transaction_id,
        receipt=issued.receipt,
        expires_at=issued.expires_at,
    )


@router.post("/orders/verify", response_model=OrderVerifyResponse)
async def verify_order(payload: OrderVerifyRequest, session: AsyncSession = Depends(get_db_session)) -> OrderVerifyResponse:
    user = await db_business.get_current_user(session)
    verification_status = verify_payment_receipt(
        user_id=user.id,
        platform=payload.platform,
        product_id=payload.product_id,
        transaction_id=payload.transaction_id,
        receipt=payload.receipt,
    )
    order, user_profile = await db_business.verify_membership_order(
        session,
        payload.platform,
        payload.product_id,
        payload.transaction_id,
        verification_status,
    )
    return OrderVerifyResponse(order=order, user=user_profile)


@router.post("/membership/orders/verify", response_model=OrderVerifyResponse)
async def verify_membership_order(payload: OrderVerifyRequest, session: AsyncSession = Depends(get_db_session)) -> OrderVerifyResponse:
    return await verify_order(payload, session)
