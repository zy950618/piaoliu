from collections.abc import Callable

from fastapi import Depends, Header, HTTPException, status

from app.security import AdminPrincipal, authenticate_admin_token, principal_has_role


def get_current_admin(authorization: str | None = Header(default=None)) -> AdminPrincipal:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "ADMIN_UNAUTHORIZED", "message": "Admin bearer token is required"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = authorization.removeprefix("Bearer ").strip()
    principal = authenticate_admin_token(token)
    if principal is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": "ADMIN_UNAUTHORIZED", "message": "Invalid admin token"},
            headers={"WWW-Authenticate": "Bearer"},
        )
    return principal


def require_admin_role(*roles: str) -> Callable[[AdminPrincipal], AdminPrincipal]:
    allowed_roles = set(roles)

    def dependency(principal: AdminPrincipal = Depends(get_current_admin)) -> AdminPrincipal:
        if allowed_roles and not principal_has_role(principal, allowed_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "ADMIN_FORBIDDEN", "message": "Admin role is not allowed"},
            )
        return principal

    return dependency
