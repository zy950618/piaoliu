from __future__ import annotations

import base64
import hashlib
import hmac
import json
import secrets
import time
from dataclasses import dataclass
from datetime import UTC, datetime

from fastapi import HTTPException

from app.settings import Settings, get_settings


DEVELOPMENT_ENVIRONMENTS = {"mock", "dev", "development", "test"}


@dataclass(frozen=True)
class MockPaymentReceipt:
    transaction_id: str
    receipt: str
    expires_at: str


def mock_payments_enabled(settings: Settings | None = None) -> bool:
    return (settings or get_settings()).environment.lower() in DEVELOPMENT_ENVIRONMENTS


def issue_mock_payment_receipt(
    *,
    user_id: str,
    platform: str,
    product_id: str,
    settings: Settings | None = None,
) -> MockPaymentReceipt:
    active_settings = settings or get_settings()
    _require_mock_environment(active_settings)
    issued_at = int(time.time())
    expires_at = issued_at + active_settings.payment_mock_ttl_seconds
    transaction_id = f"mockpay_{secrets.token_urlsafe(18)}"
    payload = {
        "exp": expires_at,
        "iat": issued_at,
        "platform": platform,
        "product_id": product_id,
        "transaction_id": transaction_id,
        "user_id": user_id,
        "version": 1,
    }
    encoded_payload = _encode(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode())
    signature = _sign(encoded_payload, active_settings.payment_mock_secret)
    return MockPaymentReceipt(
        transaction_id=transaction_id,
        receipt=f"{encoded_payload}.{signature}",
        expires_at=datetime.fromtimestamp(expires_at, UTC).isoformat(),
    )


def verify_payment_receipt(
    *,
    user_id: str,
    platform: str,
    product_id: str,
    transaction_id: str,
    receipt: str,
    settings: Settings | None = None,
) -> str:
    active_settings = settings or get_settings()
    _require_mock_environment(active_settings)
    try:
        encoded_payload, supplied_signature = receipt.split(".", 1)
    except ValueError as exc:
        raise _invalid_receipt() from exc
    expected_signature = _sign(encoded_payload, active_settings.payment_mock_secret)
    if not hmac.compare_digest(supplied_signature, expected_signature):
        raise _invalid_receipt()
    try:
        payload = json.loads(_decode(encoded_payload))
    except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise _invalid_receipt() from exc

    expected = {
        "user_id": user_id,
        "platform": platform,
        "product_id": product_id,
        "transaction_id": transaction_id,
        "version": 1,
    }
    if any(payload.get(key) != value for key, value in expected.items()):
        raise HTTPException(
            status_code=409,
            detail={"code": "PAYMENT_RECEIPT_MISMATCH", "message": "支付凭证与当前账号或套餐不匹配，请重新发起支付。"},
        )
    if not isinstance(payload.get("exp"), int) or payload["exp"] < int(time.time()):
        raise HTTPException(
            status_code=410,
            detail={"code": "PAYMENT_RECEIPT_EXPIRED", "message": "支付凭证已过期，请重新发起支付。"},
        )
    return "mock_verified"


def _require_mock_environment(settings: Settings) -> None:
    if not mock_payments_enabled(settings):
        raise HTTPException(
            status_code=503,
            detail={
                "code": "PAYMENT_PROVIDER_NOT_CONFIGURED",
                "message": "支付服务尚未配置，生产环境不会接受模拟支付凭证。",
            },
        )


def _invalid_receipt() -> HTTPException:
    return HTTPException(
        status_code=422,
        detail={"code": "PAYMENT_RECEIPT_INVALID", "message": "支付凭证校验失败，请重新发起支付。"},
    )


def _sign(encoded_payload: str, secret: str) -> str:
    return hmac.new(secret.encode(), encoded_payload.encode(), hashlib.sha256).hexdigest()


def _encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode().rstrip("=")


def _decode(value: str) -> str:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(f"{value}{padding}").decode()
