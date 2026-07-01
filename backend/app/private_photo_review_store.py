import json
from datetime import UTC, datetime
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import db_business
from app.audit import record_admin_audit
from app.models import PrivatePhotoAsset
from app.schemas import (
    AdminPrivatePhotoReviewOut,
    AdminPrivatePhotoReviewRequest,
    AdminPrivatePhotoReviewResponse,
    AdminPrivatePhotoRiskSummary,
    PrivatePhotoAppealRequest,
    PrivatePhotoAppealResponse,
    PrivatePhotoCreateRequest,
    PrivatePhotoReviewOut,
    PrivatePhotoUnlockNewResponse,
)


def iso_now() -> str:
    return datetime.now(UTC).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex}"


def current_user_id() -> str:
    return db_business.current_user_id()


def error(status_code: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"code": code, "message": message})


def classify(payload: PrivatePhotoCreateRequest) -> tuple[str, str, list[str], float, str, str, str]:
    text = f"{payload.file_id or ''} {payload.upload_token or ''} {payload.caption or ''}".lower()
    if any(word in text for word in ("minor", "fraud", "scam", "nude", "high")):
        action = "freeze" if "minor" in text or "fraud" in text else "reject"
        status = "frozen" if action == "freeze" else "rejected"
        return status, "high_risk", ["high_risk", "safety_violation"], 0.96, action, "ineligible", "内容风险较高，已拒绝或冻结并进入风险队列。"
    if any(word in text for word in ("manual", "borderline", "low_confidence", "blur")):
        return "manual_required", "medium_risk", ["low_confidence", "borderline_content"], 0.62, "manual_review", "frozen", "内容需要人工复核，复核前不会展示或产生收益。"
    return "ai_approved", "low_risk", ["non_explicit", "no_sensitive_privacy"], 0.93, "approve", "eligible", "AI 审核已通过，可以展示并按规则产生收益。"


def cover_tone_for(risk_level: str) -> str:
    return {"low_risk": "mint", "medium_risk": "amber", "high_risk": "rose"}.get(risk_level, "mint")


def encode_list(values: list[str]) -> str:
    return json.dumps(values, ensure_ascii=False)


def decode_list(value: str | None) -> list[str]:
    if not value:
        return []
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return [item for item in value.split(",") if item]
    return parsed if isinstance(parsed, list) else []


def encode_dict(value: dict[str, str] | None) -> str | None:
    return json.dumps(value, ensure_ascii=False) if value else None


def decode_dict(value: str | None) -> dict[str, str] | None:
    if not value:
        return None
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


def review_status(value: str) -> str:
    return "ai_approved" if value == "approved" else value


def record_photo_audit(
    session: AsyncSession,
    actor: str,
    action: str,
    target_id: str,
    detail: str | None = None,
):
    audit_id = db_business.new_id("audit")
    audit = record_admin_audit(actor, action, "private_photo", target_id, audit_id=audit_id)
    session.add(
        db_business.AdminAuditLog(
            id=audit.id,
            actor=audit.actor,
            action=audit.action,
            target_type=audit.target_type,
            target_id=audit.target_id,
            detail=detail,
            created_at=db_business.now(),
        )
    )
    return audit


async def create_photo(session: AsyncSession, payload: PrivatePhotoCreateRequest) -> PrivatePhotoReviewOut:
    if not payload.file_id and not payload.upload_token:
        raise error(422, "PHOTO_FILE_REQUIRED", "file_id or upload_token is required")

    await db_business.get_current_user(session)
    if payload.client_upload_id:
        existing = await session.scalar(
            select(PrivatePhotoAsset).where(PrivatePhotoAsset.client_upload_id == payload.client_upload_id)
        )
        if existing is not None:
            return to_public(existing)

    owner = await session.get(db_business.User, current_user_id())
    photo_id = new_id("photo_review")
    status, risk_level, labels, confidence, auto_action, revenue_state, message = classify(payload)
    audit = record_photo_audit(
        session,
        current_user_id(),
        f"private_photo_ai_{auto_action}",
        photo_id,
        detail=f"risk_level={risk_level};auto_action={auto_action}",
    )
    now_ts = db_business.now()
    row = PrivatePhotoAsset(
        id=photo_id,
        owner_id=current_user_id(),
        owner_name=owner.nickname if owner else "匿名用户",
        title=payload.caption or payload.file_id or payload.upload_token or photo_id,
        cover_tone=cover_tone_for(risk_level),
        price_coins=30,
        status=status,
        purchased_by_user_ids="",
        file_id=payload.file_id,
        upload_token=payload.upload_token,
        client_upload_id=payload.client_upload_id,
        risk_level=risk_level,
        model_labels=encode_list(labels),
        confidence=f"{confidence:.2f}",
        auto_action=auto_action,
        revenue_state=revenue_state,
        user_visible_message=message,
        manual_review=None,
        appeal_state=None,
        report_count=0,
        assigned_admin_id=None,
        audit_refs=encode_list([audit.id]),
        created_at=now_ts,
        updated_at=now_ts,
    )
    session.add(row)
    await session.commit()
    await session.refresh(row)
    return to_public(row)


async def list_photos(
    session: AsyncSession,
    review_status: str | None = None,
    risk_level: str | None = None,
) -> list[PrivatePhotoReviewOut]:
    await db_business.get_current_user(session)
    query = select(PrivatePhotoAsset).where(PrivatePhotoAsset.owner_id == current_user_id())
    if review_status:
        query = query.where(PrivatePhotoAsset.status == review_status)
    if risk_level:
        query = query.where(PrivatePhotoAsset.risk_level == risk_level)
    rows = (await session.execute(query.order_by(PrivatePhotoAsset.created_at.desc()))).scalars().all()
    return [to_public(row) for row in rows]


async def get_photo(session: AsyncSession, photo_id: str) -> PrivatePhotoReviewOut:
    await db_business.get_current_user(session)
    row = await session.get(PrivatePhotoAsset, photo_id)
    if row is None or row.owner_id != current_user_id():
        raise error(404, "PHOTO_REVIEW_NOT_FOUND", "Private photo not found")
    return to_public(row)


async def unlock_photo(session: AsyncSession, photo_id: str) -> PrivatePhotoUnlockNewResponse:
    await db_business.get_current_user(session)
    row = await session.get(PrivatePhotoAsset, photo_id)
    if row is None:
        raise error(404, "PHOTO_REVIEW_NOT_FOUND", "Private photo not found")
    if row.status in {"ai_pending", "manual_required", "appeal_pending"}:
        raise error(409, "PHOTO_REVIEW_PENDING", "Photo review is not complete")
    if row.status == "rejected":
        raise error(409, "PHOTO_REJECTED", "Rejected photo cannot be unlocked")
    if row.status == "frozen":
        raise error(409, "PHOTO_FROZEN", "Frozen photo cannot be unlocked")
    if row.revenue_state != "eligible":
        raise error(409, "PHOTO_REVENUE_FROZEN", "Photo revenue is not eligible")

    unlock_id = new_id("unlock")
    audit = record_photo_audit(session, current_user_id(), "private_photo_unlock", photo_id)
    row.audit_refs = encode_list([*decode_list(row.audit_refs), audit.id])
    row.updated_at = db_business.now()
    await session.commit()
    return PrivatePhotoUnlockNewResponse(
        unlock_id=unlock_id,
        photo_id=photo_id,
        charged_amount=30,
        creator_revenue_state=row.revenue_state,
        audit_id=audit.id,
    )


async def appeal_photo(
    session: AsyncSession,
    photo_id: str,
    payload: PrivatePhotoAppealRequest,
) -> PrivatePhotoAppealResponse:
    await db_business.get_current_user(session)
    row = await session.get(PrivatePhotoAsset, photo_id)
    if row is None or row.owner_id != current_user_id():
        raise error(404, "PHOTO_REVIEW_NOT_FOUND", "Private photo not found")
    if row.status not in {"rejected", "frozen"}:
        raise error(409, "PHOTO_APPEAL_NOT_ALLOWED", "Only rejected or frozen photos can be appealed")

    before_refs = decode_list(row.audit_refs)
    audit = record_photo_audit(session, current_user_id(), "private_photo_appeal", photo_id, detail=payload.reason)
    row.status = "appeal_pending"
    row.revenue_state = "frozen"
    row.appeal_state = f"pending:{payload.reason}"
    row.audit_refs = encode_list([*before_refs, audit.id])
    row.updated_at = db_business.now()
    await session.commit()
    return PrivatePhotoAppealResponse(
        photo_id=photo_id,
        review_status=review_status(row.status),
        appeal_state=row.appeal_state,
        revenue_state=row.revenue_state,
        audit_id=audit.id,
    )


async def admin_reviews(
    session: AsyncSession,
    review_status: str | None = None,
    risk_level: str | None = None,
    user_id: str | None = None,
) -> list[AdminPrivatePhotoReviewOut]:
    query = select(PrivatePhotoAsset)
    if review_status:
        query = query.where(PrivatePhotoAsset.status == review_status)
    if risk_level:
        query = query.where(PrivatePhotoAsset.risk_level == risk_level)
    if user_id:
        query = query.where(PrivatePhotoAsset.owner_id == user_id)
    rows = (await session.execute(query.order_by(PrivatePhotoAsset.updated_at.desc()))).scalars().all()
    return [to_admin(row) for row in rows]


async def admin_review_detail(session: AsyncSession, review_id: str) -> AdminPrivatePhotoReviewOut:
    row = await session.get(PrivatePhotoAsset, review_id)
    if row is None:
        raise error(404, "PHOTO_REVIEW_NOT_FOUND", "Review not found")
    return to_admin(row)


async def apply_admin_review(
    session: AsyncSession,
    review_id: str,
    payload: AdminPrivatePhotoReviewRequest,
) -> AdminPrivatePhotoReviewResponse:
    row = await session.get(PrivatePhotoAsset, review_id)
    if row is None:
        raise error(404, "PHOTO_REVIEW_NOT_FOUND", "Review not found")

    before_status = row.status
    before_revenue = row.revenue_state
    if payload.action == "approve":
        row.status = "manual_approved"
        row.revenue_state = "eligible" if payload.revenue_action == "release" else row.revenue_state
    elif payload.action == "reject":
        row.status = "rejected"
        row.revenue_state = "ineligible"
    elif payload.action == "freeze":
        row.status = "frozen"
        row.revenue_state = "frozen"
    elif payload.action == "unfreeze":
        row.status = "manual_approved"
        row.revenue_state = "eligible" if payload.revenue_action == "release" else "frozen"
    else:
        row.status = "manual_required"
        row.revenue_state = "frozen"

    row.manual_review = encode_dict({"action": payload.action, "reason": payload.reason})
    row.model_labels = encode_list(sorted(set(decode_list(row.model_labels) + payload.manual_labels)))
    row.updated_at = db_business.now()
    audit = record_photo_audit(
        session,
        "admin",
        f"private_photo_review_{payload.action}",
        review_id,
        detail=payload.reason,
    )
    row.audit_refs = encode_list([*decode_list(row.audit_refs), audit.id])
    await session.commit()
    return AdminPrivatePhotoReviewResponse(
        review_id=review_id,
        before_status=before_status,
        after_status=row.status,
        before_revenue_state=before_revenue,
        after_revenue_state=row.revenue_state,
        audit_id=audit.id,
    )


async def risk_summary(session: AsyncSession) -> AdminPrivatePhotoRiskSummary:
    rows = (await session.execute(select(PrivatePhotoAsset))).scalars().all()
    return AdminPrivatePhotoRiskSummary(
        low_risk=sum(1 for row in rows if row.risk_level == "low_risk"),
        medium_risk=sum(1 for row in rows if row.risk_level == "medium_risk"),
        high_risk=sum(1 for row in rows if row.risk_level == "high_risk"),
        manual_required=sum(1 for row in rows if row.status == "manual_required"),
        frozen=sum(1 for row in rows if row.status == "frozen"),
    )


def to_public(row: PrivatePhotoAsset) -> PrivatePhotoReviewOut:
    return PrivatePhotoReviewOut(
        id=row.id,
        owner_id=row.owner_id,
        review_status=review_status(row.status),
        risk_level=row.risk_level,
        model_labels=decode_list(row.model_labels),
        confidence=float(row.confidence or 0),
        auto_action=row.auto_action,
        revenue_state=row.revenue_state,
        user_visible_message=row.user_visible_message,
        created_at=db_business.iso(row.created_at),
        manual_review=decode_dict(row.manual_review),
        appeal_state=row.appeal_state,
        audit_refs=decode_list(row.audit_refs),
    )


def to_admin(row: PrivatePhotoAsset) -> AdminPrivatePhotoReviewOut:
    return AdminPrivatePhotoReviewOut(
        id=row.id,
        photo_id=row.id,
        user_id=row.owner_id,
        review_status=review_status(row.status),
        risk_level=row.risk_level,
        model_labels=decode_list(row.model_labels),
        confidence=float(row.confidence or 0),
        auto_action=row.auto_action,
        report_count=row.report_count,
        revenue_state=row.revenue_state,
        assigned_admin_id=row.assigned_admin_id,
        updated_at=db_business.iso(row.updated_at or row.created_at),
    )
