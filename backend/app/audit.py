from app.mock_store import iso_now
from app.schemas import AdminAuditLogOut

_audit_logs = [
    AdminAuditLogOut(
        id="audit_001",
        actor="system",
        action="mock_bootstrap",
        target_type="system",
        target_id="backend",
        created_at=iso_now(),
    )
]


def record_admin_audit(actor: str, action: str, target_type: str, target_id: str) -> AdminAuditLogOut:
    entry = AdminAuditLogOut(
        id=f"audit_{len(_audit_logs) + 1:03d}",
        actor=actor,
        action=action,
        target_type=target_type,
        target_id=target_id,
        created_at=iso_now(),
    )
    _audit_logs.insert(0, entry)
    return entry


def list_admin_audit_logs() -> list[AdminAuditLogOut]:
    return _audit_logs
