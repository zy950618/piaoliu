from secrets import compare_digest
import hashlib
import hmac
import time

from pydantic import BaseModel

from app.settings import get_settings


class AdminPrincipal(BaseModel):
    username: str
    roles: list[str]


def _admin_accounts() -> dict[str, tuple[str, list[str]]]:
    settings = get_settings()
    accounts: dict[str, tuple[str, list[str]]] = {}
    for item in settings.admin_accounts.split(";"):
        parts = [part.strip() for part in item.split(":", 2)]
        if len(parts) != 3 or not parts[0] or not parts[1]:
            continue
        roles = [role.strip() for role in parts[2].split(",") if role.strip()]
        if roles:
            accounts[parts[0]] = (parts[1], roles)
    if settings.admin_mock_username not in accounts:
        accounts[settings.admin_mock_username] = (
            settings.admin_mock_password,
            ["admin", "moderator"],
        )
    return accounts


def _token_signature(username: str, expires_at: int) -> str:
    settings = get_settings()
    return hmac.new(
        settings.admin_token_secret.encode("utf-8"),
        f"{username}:{expires_at}".encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def create_admin_token(username: str, password: str) -> str | None:
    account = _admin_accounts().get(username)
    if account and compare_digest(password, account[0]):
        expires_at = int(time.time()) + get_settings().admin_token_expires_seconds
        return f"admin-session:{username}:{expires_at}:{_token_signature(username, expires_at)}"
    return None


def authenticate_admin_token(token: str) -> AdminPrincipal | None:
    settings = get_settings()
    if settings.environment in {"mock", "dev", "development", "test"} and compare_digest(token, settings.admin_mock_token):
        return AdminPrincipal(username=settings.admin_mock_username, roles=["admin", "moderator"])
    prefix = "admin-session:"
    if not token.startswith(prefix):
        return None
    try:
        username, expires_text, signature = token.removeprefix(prefix).split(":", 2)
    except ValueError:
        return None
    try:
        expires_at = int(expires_text)
    except ValueError:
        return None
    if expires_at <= int(time.time()):
        return None
    account = _admin_accounts().get(username)
    if account is None:
        return None
    if not compare_digest(signature, _token_signature(username, expires_at)):
        return None
    return AdminPrincipal(username=username, roles=account[1])
    return None


def principal_has_role(principal: AdminPrincipal, allowed_roles: set[str]) -> bool:
    effective_roles = set(principal.roles)
    if "super_admin" in effective_roles:
        effective_roles.update({"admin", "operator", "moderator", "risk", "viewer"})
    if "operator" in effective_roles:
        effective_roles.update({"admin", "viewer"})
    if "moderator" in effective_roles or "risk" in effective_roles:
        effective_roles.add("viewer")
    return bool(effective_roles & allowed_roles)
