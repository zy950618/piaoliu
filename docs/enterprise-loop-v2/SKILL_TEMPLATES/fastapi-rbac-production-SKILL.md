---
name: fastapi-rbac-production
description: Implements production-grade FastAPI admin authentication, RBAC, sessions/tokens, errors, and permission tests.
---

# FastAPI RBAC Production

## Must include

- Admin model.
- Password hash.
- Session/token persistence.
- Roles and permissions.
- API guards.
- Unauthorized/forbidden errors.
- Audit logs.
- Tests for each role.

## Forbidden

- Plaintext passwords.
- Frontend-only permission checks.
- Mock token claimed as production.
