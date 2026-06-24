"""add plaza comment visibility flag

Revision ID: 0005_plaza_comment_visibility
Revises: 0004_plaza_posts_media_comments
Create Date: 2026-06-24
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "0005_plaza_comment_visibility"
down_revision: str | None = "0004_plaza_posts_media_comments"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "plaza_comments",
        sa.Column("hidden_for_owner_only", sa.Boolean(), nullable=False, server_default=sa.false()),
    )


def downgrade() -> None:
    op.drop_column("plaza_comments", "hidden_for_owner_only")
