from fastapi import APIRouter

from app.mock_store import consume_quota, get_status
from app.schemas import ConsumeQuotaRequest, QuotaItem, QuotaType

router = APIRouter(prefix="/quota", tags=["quota"])


@router.get("/today", response_model=dict[QuotaType, QuotaItem])
def quota_today() -> dict[QuotaType, QuotaItem]:
    return get_status().quotas


@router.post("/consume", response_model=QuotaItem)
def quota_consume(payload: ConsumeQuotaRequest) -> QuotaItem:
    return consume_quota(payload.quota_type, payload.business_id)
