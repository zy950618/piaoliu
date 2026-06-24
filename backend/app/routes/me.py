from fastapi import APIRouter

from app.mock_store import get_status
from app.schemas import MeStatus

router = APIRouter(tags=["me"])


@router.get("/me/status", response_model=MeStatus)
def me_status() -> MeStatus:
    return get_status()


@router.get("/users/me/status", response_model=MeStatus)
def user_status() -> MeStatus:
    return get_status()
