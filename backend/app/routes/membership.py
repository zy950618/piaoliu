from fastapi import APIRouter

from app import mock_store
from app.schemas import MembershipOrderOut, MembershipProduct, OrderVerifyRequest, OrderVerifyResponse

router = APIRouter(tags=["membership"])


@router.get("/membership/products", response_model=list[MembershipProduct])
def membership_products() -> list[MembershipProduct]:
    benefits = ["每日次数增加", "会员身份标识", "专属装扮", "历史记录扩容"]
    return [
        MembershipProduct(id="vip_month", name="月卡会员", price_label="¥18", platform="all", benefits=benefits),
        MembershipProduct(id="vip_season", name="季卡会员", price_label="¥45", platform="all", benefits=benefits),
        MembershipProduct(id="vip_year", name="年卡会员", price_label="¥128", platform="all", benefits=benefits),
    ]


@router.get("/orders", response_model=list[MembershipOrderOut])
def list_orders() -> list[MembershipOrderOut]:
    return list(mock_store.orders_by_transaction.values())


@router.get("/membership/orders", response_model=list[MembershipOrderOut])
def list_membership_orders() -> list[MembershipOrderOut]:
    return list_orders()


@router.post("/orders/verify", response_model=OrderVerifyResponse)
def verify_order(payload: OrderVerifyRequest) -> OrderVerifyResponse:
    order = mock_store.verify_membership_order(payload.platform, payload.product_id, payload.transaction_id)
    return OrderVerifyResponse(order=order, user=mock_store.user)


@router.post("/membership/orders/verify", response_model=OrderVerifyResponse)
def verify_membership_order(payload: OrderVerifyRequest) -> OrderVerifyResponse:
    return verify_order(payload)
