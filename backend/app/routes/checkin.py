from fastapi import APIRouter

from app.mock_store import checkin, checkin_today
from app.schemas import CheckinState

router = APIRouter(prefix="/checkin", tags=["checkin"])


@router.post("", response_model=CheckinState)
def post_checkin() -> CheckinState:
    return checkin_today()


@router.get("/week", response_model=CheckinState)
def get_checkin_week() -> CheckinState:
    return checkin
