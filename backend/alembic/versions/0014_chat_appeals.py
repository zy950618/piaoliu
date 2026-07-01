"""chat appeals

Revision ID: 0014_chat_appeals
Revises: 0013_app_configs_ad_reward
Create Date: 2026-07-01 00:10:00
"""

from alembic import op
import sqlalchemy as sa

revision = "0014_chat_appeals"
down_revision = "0013_app_configs_ad_reward"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "chat_appeals",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("thread_id", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.String(length=64), nullable=False),
        sa.Column("reason", sa.String(length=240), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False),
        sa.Column("admin_reason", sa.String(length=240), nullable=True),
        sa.Column("audit_refs", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["thread_id"], ["conversation_threads.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("thread_id", "user_id", "status", name="uq_chat_appeals_open_once"),
    )
    op.create_index(op.f("ix_chat_appeals_thread_id"), "chat_appeals", ["thread_id"], unique=False)
    op.create_index(op.f("ix_chat_appeals_user_id"), "chat_appeals", ["user_id"], unique=False)
    op.create_index(op.f("ix_chat_appeals_status"), "chat_appeals", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_chat_appeals_status"), table_name="chat_appeals")
    op.drop_index(op.f("ix_chat_appeals_user_id"), table_name="chat_appeals")
    op.drop_index(op.f("ix_chat_appeals_thread_id"), table_name="chat_appeals")
    op.drop_table("chat_appeals")
