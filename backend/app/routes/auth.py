import hashlib

import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app import db_business
from app.settings import get_settings
from app.user_security import issue_user_token


router = APIRouter(prefix="/auth", tags=["auth"])


class WechatLoginRequest(BaseModel):
    code: str = Field(min_length=3, max_length=256)


class WechatLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: int
    user_id: str
    mock: bool


async def exchange_wechat_code(code: str) -> tuple[str, bool]:
    settings = get_settings()
    if settings.environment in {"mock", "dev", "development", "test"}:
        return f"dev:{code}", True
    if not settings.wechat_app_id or not settings.wechat_app_secret:
        raise HTTPException(
            status_code=503,
            detail={"code": "WECHAT_NOT_CONFIGURED", "message": "微信登录尚未配置，请联系管理员完成 AppID 和密钥配置"},
        )
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(
                "https://api.weixin.qq.com/sns/jscode2session",
                params={
                    "appid": settings.wechat_app_id,
                    "secret": settings.wechat_app_secret,
                    "js_code": code,
                    "grant_type": "authorization_code",
                },
            )
            response.raise_for_status()
            payload = response.json()
    except (httpx.HTTPError, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail={"code": "WECHAT_LOGIN_UNAVAILABLE", "message": "微信登录服务暂时不可用，请稍后重试"},
        ) from exc
    openid = payload.get("openid")
    if not openid:
        raise HTTPException(
            status_code=401,
            detail={"code": "WECHAT_CODE_INVALID", "message": "微信登录凭证已失效，请重新登录"},
        )
    return str(openid), False


@router.post("/wechat", response_model=WechatLoginResponse)
async def login_with_wechat(payload: WechatLoginRequest) -> WechatLoginResponse:
    identity, is_mock = await exchange_wechat_code(payload.code)
    digest = hashlib.sha256(identity.encode("utf-8")).hexdigest()
    user_id = db_business.normalize_user_id(f"wechat:{digest}")
    token, expires_at = issue_user_token(user_id)
    return WechatLoginResponse(
        access_token=token,
        expires_at=expires_at,
        user_id=user_id,
        mock=is_mock,
    )
