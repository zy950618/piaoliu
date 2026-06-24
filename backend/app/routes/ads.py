from fastapi import APIRouter

from app.mock_store import ad_reward, commit_ad_reward, prepare_ad_reward
from app.schemas import AdCommitRequest, AdPrepareResponse, AdRewardState, MeStatus

router = APIRouter(prefix="/ads/reward", tags=["ads"])


@router.get("/status", response_model=AdRewardState)
def reward_status() -> AdRewardState:
    return ad_reward


@router.post("/prepare", response_model=AdPrepareResponse)
def reward_prepare() -> AdPrepareResponse:
    return AdPrepareResponse(reward_session_id=prepare_ad_reward(), reward_per_quota=ad_reward.reward_per_quota)


@router.post("/commit", response_model=MeStatus)
def reward_commit(payload: AdCommitRequest) -> MeStatus:
    return commit_ad_reward(payload.reward_session_id, payload.completed)
