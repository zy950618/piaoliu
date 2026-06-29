"""add prompt templates

Revision ID: 0009_prompt_templates
Revises: 0008_user_activity_records
Create Date: 2026-06-26
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "0009_prompt_templates"
down_revision: str | None = "0008_user_activity_records"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "prompt_templates",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("prompt_type", sa.String(length=32), nullable=False),
        sa.Column("mode", sa.String(length=40), nullable=True),
        sa.Column("category", sa.String(length=40), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("meaning", sa.Text(), nullable=True),
        sa.Column("visibility", sa.String(length=40), nullable=True),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="active"),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_prompt_templates_prompt_type", "prompt_templates", ["prompt_type"])
    op.create_index("ix_prompt_templates_mode", "prompt_templates", ["mode"])


def downgrade() -> None:
    op.drop_index("ix_prompt_templates_mode", table_name="prompt_templates")
    op.drop_index("ix_prompt_templates_prompt_type", table_name="prompt_templates")
    op.drop_table("prompt_templates")
