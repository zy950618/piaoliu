"""add plaza posts media comments and likes

Revision ID: 0004_plaza_posts_media_comments
Revises: 0003_bottle_target_scope
Create Date: 2026-06-24
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "0004_plaza_posts_media_comments"
down_revision: str | None = "0003_bottle_target_scope"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "plaza_posts",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("author_id", sa.String(length=64), nullable=False),
        sa.Column("author_name", sa.String(length=80), nullable=False),
        sa.Column("icon_text", sa.String(length=8), nullable=False),
        sa.Column("topic", sa.String(length=40), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("media_type", sa.String(length=16), nullable=False, server_default="text"),
        sa.Column("media_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("gender", sa.String(length=16), nullable=False, server_default="unknown"),
        sa.Column("verified", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("city", sa.String(length=40), nullable=True),
        sa.Column("age_range", sa.String(length=24), nullable=True),
        sa.Column("view_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("like_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("comment_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("comment_preview", sa.String(length=160), nullable=True),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="approved"),
        sa.Column("distance_text", sa.String(length=40), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_plaza_posts_author_id", "plaza_posts", ["author_id"])
    op.create_index("ix_plaza_posts_city", "plaza_posts", ["city"])
    op.create_index("ix_plaza_posts_age_range", "plaza_posts", ["age_range"])

    op.create_table(
        "plaza_media",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("post_id", sa.String(length=64), nullable=False),
        sa.Column("owner_id", sa.String(length=64), nullable=False),
        sa.Column("media_type", sa.String(length=16), nullable=False),
        sa.Column("url", sa.String(length=500), nullable=False),
        sa.Column("storage_key", sa.String(length=240), nullable=False),
        sa.Column("mime_type", sa.String(length=120), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=True),
        sa.Column("duration_seconds", sa.Integer(), nullable=True),
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["post_id"], ["plaza_posts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_plaza_media_owner_id", "plaza_media", ["owner_id"])
    op.create_index("ix_plaza_media_post_id", "plaza_media", ["post_id"])

    op.create_table(
        "plaza_comments",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("post_id", sa.String(length=64), nullable=False),
        sa.Column("author_id", sa.String(length=64), nullable=False),
        sa.Column("author_name", sa.String(length=80), nullable=False),
        sa.Column("icon_text", sa.String(length=8), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="approved"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["post_id"], ["plaza_posts.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_plaza_comments_author_id", "plaza_comments", ["author_id"])
    op.create_index("ix_plaza_comments_post_id", "plaza_comments", ["post_id"])

    op.create_table(
        "plaza_likes",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("post_id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["post_id"], ["plaza_posts.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("post_id", "user_id", name="uq_plaza_likes_post_user"),
    )
    op.create_index("ix_plaza_likes_post_id", "plaza_likes", ["post_id"])
    op.create_index("ix_plaza_likes_user_id", "plaza_likes", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_plaza_likes_user_id", table_name="plaza_likes")
    op.drop_index("ix_plaza_likes_post_id", table_name="plaza_likes")
    op.drop_table("plaza_likes")
    op.drop_index("ix_plaza_comments_post_id", table_name="plaza_comments")
    op.drop_index("ix_plaza_comments_author_id", table_name="plaza_comments")
    op.drop_table("plaza_comments")
    op.drop_index("ix_plaza_media_post_id", table_name="plaza_media")
    op.drop_index("ix_plaza_media_owner_id", table_name="plaza_media")
    op.drop_table("plaza_media")
    op.drop_index("ix_plaza_posts_age_range", table_name="plaza_posts")
    op.drop_index("ix_plaza_posts_city", table_name="plaza_posts")
    op.drop_index("ix_plaza_posts_author_id", table_name="plaza_posts")
    op.drop_table("plaza_posts")
