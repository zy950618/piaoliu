"""add user activity records

Revision ID: 0008_user_activity_records
Revises: 0007_business_runtime_tables
Create Date: 2026-06-26
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "0008_user_activity_records"
down_revision: str | None = "0007_business_runtime_tables"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "user_activity_records",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("user_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("record_type", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=80), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("visibility", sa.String(length=40), nullable=True),
        sa.Column("source_type", sa.String(length=40), nullable=True),
        sa.Column("source_id", sa.String(length=80), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_user_activity_records_user_id", "user_activity_records", ["user_id"])
    op.create_index("ix_user_activity_records_record_type", "user_activity_records", ["record_type"])


def downgrade() -> None:
    op.drop_index("ix_user_activity_records_record_type", table_name="user_activity_records")
    op.drop_index("ix_user_activity_records_user_id", table_name="user_activity_records")
    op.drop_table("user_activity_records")
