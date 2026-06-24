"""add bottle and relation models

Revision ID: 0002_bottle_relation_models
Revises: 0001_initial_admin_auth_audit
Create Date: 2026-06-23
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "0002_bottle_relation_models"
down_revision: str | None = "0001_initial_admin_auth_audit"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "bottles",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("author_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("author_name", sa.String(length=80), nullable=False),
        sa.Column("author_avatar_text", sa.String(length=8), nullable=True),
        sa.Column("author_vip", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("author_gender", sa.String(length=16), nullable=False, server_default="unknown"),
        sa.Column("author_age_range", sa.String(length=24), nullable=True),
        sa.Column("author_city", sa.String(length=40), nullable=True),
        sa.Column("author_verified", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("mood", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="pending"),
        sa.Column("replies", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("target_gender", sa.String(length=16), nullable=False, server_default="all"),
        sa.Column("target_city", sa.String(length=40), nullable=False, server_default="全国"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_bottles_author_id", "bottles", ["author_id"])
    op.create_index("ix_bottles_status_created_at", "bottles", ["status", "created_at"])

    op.create_table(
        "bottle_replies",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("bottle_id", sa.String(length=64), sa.ForeignKey("bottles.id"), nullable=False),
        sa.Column("author_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_bottle_replies_bottle_id", "bottle_replies", ["bottle_id"])
    op.create_index("ix_bottle_replies_author_id", "bottle_replies", ["author_id"])

    op.create_table(
        "follows",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("follower_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("target_user_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_follows_follower_id", "follows", ["follower_id"])
    op.create_index("ix_follows_target_user_id", "follows", ["target_user_id"])
    op.create_unique_constraint("uq_follows_follower_target", "follows", ["follower_id", "target_user_id"])


def downgrade() -> None:
    op.drop_constraint("uq_follows_follower_target", "follows", type_="unique")
    op.drop_index("ix_follows_target_user_id", table_name="follows")
    op.drop_index("ix_follows_follower_id", table_name="follows")
    op.drop_table("follows")

    op.drop_index("ix_bottle_replies_author_id", table_name="bottle_replies")
    op.drop_index("ix_bottle_replies_bottle_id", table_name="bottle_replies")
    op.drop_table("bottle_replies")

    op.drop_index("ix_bottles_status_created_at", table_name="bottles")
    op.drop_index("ix_bottles_author_id", table_name="bottles")
    op.drop_table("bottles")
