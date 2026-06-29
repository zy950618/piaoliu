"""add membership product configs

Revision ID: 0010_membership_product_configs
Revises: 0009_prompt_templates
Create Date: 2026-06-26
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "0010_membership_product_configs"
down_revision: str | None = "0009_prompt_templates"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "membership_product_configs",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("price_label", sa.String(length=40), nullable=False),
        sa.Column("platform", sa.String(length=24), nullable=False, server_default="all"),
        sa.Column("benefits_text", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="active"),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("membership_product_configs")
