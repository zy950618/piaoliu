import base64
import hashlib
import hmac
import json
import time
from dataclasses import dataclass

from app.settings import get_settings


@dataclass(frozen=True)
class UserSession:
    user_id: str
    expires_at: int


def _encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def issue_user_token(user_id: str) -> tuple[str, int]:
    settings = get_settings()
    expires_at = int(time.time()) + settings.user_token_expires_seconds
    body = _encode(json.dumps({"sub": user_id, "exp": expires_at}, separators=(",", ":")).encode("utf-8"))
    signature = _encode(hmac.new(settings.user_token_secret.encode("utf-8"), body.encode("ascii"), hashlib.sha256).digest())
    return f"user-session.{body}.{signature}", expires_at


def authenticate_user_token(token: str) -> UserSession | None:
    try:
        prefix, body, signature = token.split(".", 2)
    except ValueError:
        return None
    if prefix != "user-session":
        return None
    settings = get_settings()
    expected = _encode(hmac.new(settings.user_token_secret.encode("utf-8"), body.encode("ascii"), hashlib.sha256).digest())
    if not hmac.compare_digest(signature, expected):
        return None
    try:
        payload = json.loads(_decode(body))
        user_id = str(payload["sub"])
        expires_at = int(payload["exp"])
    except (KeyError, TypeError, ValueError, json.JSONDecodeError):
        return None
    if not user_id or expires_at <= int(time.time()):
        return None
    return UserSession(user_id=user_id, expires_at=expires_at)
