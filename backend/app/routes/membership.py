from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import db_business
from app.db import get_db_session
from app.schemas import MembershipOrderOut, MembershipProduct, OrderVerifyRequest, OrderVerifyResponse

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


@router.post("/orders/verify", response_model=OrderVerifyResponse)
async def verify_order(payload: OrderVerifyRequest, session: AsyncSession = Depends(get_db_session)) -> OrderVerifyResponse:
    order, user = await db_business.verify_membership_order(session, payload.platform, payload.product_id, payload.transaction_id)
    return OrderVerifyResponse(order=order, user=user)


@router.post("/membership/orders/verify", response_model=OrderVerifyResponse)
async def verify_membership_order(payload: OrderVerifyRequest, session: AsyncSession = Depends(get_db_session)) -> OrderVerifyResponse:
    return await verify_order(payload, session)
