from secrets import compare_digest

from pydantic import BaseModel

from app.settings import get_settings


class AdminPrincipal(BaseModel):
    username: str
    roles: list[str]


def create_mock_admin_token(username: str, password: str) -> str | None:
    settings = get_settings()
    username_matches = compare_digest(username, settings.admin_mock_username)
    password_matches = compare_digest(password, settings.admin_mock_password)
    if username_matches and password_matches:
        return settings.admin_mock_token
    return None


def authenticate_admin_token(token: str) -> AdminPrincipal | None:
    settings = get_settings()
    if compare_digest(token, settings.admin_mock_token):
        return AdminPrincipal(username=settings.admin_mock_username, roles=["admin", "moderator"])
    return None


def principal_has_role(principal: AdminPrincipal, allowed_roles: set[str]) -> bool:
    return bool(set(principal.roles) & allowed_roles)
