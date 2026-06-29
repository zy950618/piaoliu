"""add business runtime tables

Revision ID: 0007_business_runtime_tables
Revises: 0006_core_business_schema
Create Date: 2026-06-25
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "0007_business_runtime_tables"
down_revision: str | None = "0006_core_business_schema"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "private_photo_assets",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("owner_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("owner_name", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("cover_tone", sa.String(length=24), nullable=False, server_default="mint"),
        sa.Column("price_coins", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="approved"),
        sa.Column("purchased_by_user_ids", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_private_photo_assets_owner_id", "private_photo_assets", ["owner_id"])

    op.create_table(
        "membership_orders",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("user_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("platform", sa.String(length=24), nullable=False),
        sa.Column("product_id", sa.String(length=64), nullable=False),
        sa.Column("transaction_id", sa.String(length=120), nullable=False, unique=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="mock_verified"),
        sa.Column("vip_level", sa.String(length=24), nullable=False),
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_membership_orders_user_id", "membership_orders", ["user_id"])

    op.create_table(
        "content_reports",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("reporter_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("target_type", sa.String(length=32), nullable=False),
        sa.Column("target_id", sa.String(length=64), nullable=False),
        sa.Column("reason", sa.String(length=160), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="queued"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("reporter_id", "target_type", "target_id", "reason", name="uq_content_reports_once"),
    )
    op.create_index("ix_content_reports_reporter_id", "content_reports", ["reporter_id"])
    op.create_index("ix_content_reports_target_id", "content_reports", ["target_id"])

    op.create_table(
        "friend_requests",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("requester_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("target_user_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="requested"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("requester_id", "target_user_id", name="uq_friend_requests_pair"),
    )
    op.create_index("ix_friend_requests_requester_id", "friend_requests", ["requester_id"])
    op.create_index("ix_friend_requests_target_user_id", "friend_requests", ["target_user_id"])

    op.create_table(
        "message_notifications",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("user_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("body", sa.String(length=500), nullable=False),
        sa.Column("unread", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("business_type", sa.String(length=40), nullable=True),
        sa.Column("business_id", sa.String(length=80), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_message_notifications_user_id", "message_notifications", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_message_notifications_user_id", table_name="message_notifications")
    op.drop_table("message_notifications")
    op.drop_index("ix_friend_requests_target_user_id", table_name="friend_requests")
    op.drop_index("ix_friend_requests_requester_id", table_name="friend_requests")
    op.drop_table("friend_requests")
    op.drop_index("ix_content_reports_target_id", table_name="content_reports")
    op.drop_index("ix_content_reports_reporter_id", table_name="content_reports")
    op.drop_table("content_reports")
    op.drop_index("ix_membership_orders_user_id", table_name="membership_orders")
    op.drop_table("membership_orders")
    op.drop_index("ix_private_photo_assets_owner_id", table_name="private_photo_assets")
    op.drop_table("private_photo_assets")
