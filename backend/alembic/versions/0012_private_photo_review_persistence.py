"""private photo review persistence

Revision ID: 0012_private_photo_reviews
Revises: 0011_context_chat_persistence
Create Date: 2026-06-30 12:35:00
"""

from alembic import op
import sqlalchemy as sa

revision = "0012_private_photo_reviews"
down_revision = "0011_context_chat_persistence"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("private_photo_assets", sa.Column("file_id", sa.String(length=120), nullable=True))
    op.add_column("private_photo_assets", sa.Column("upload_token", sa.String(length=120), nullable=True))
    op.add_column("private_photo_assets", sa.Column("client_upload_id", sa.String(length=120), nullable=True))
    op.add_column("private_photo_assets", sa.Column("risk_level", sa.String(length=24), nullable=False, server_default="low_risk"))
    op.add_column("private_photo_assets", sa.Column("model_labels", sa.Text(), nullable=False, server_default=""))
    op.add_column("private_photo_assets", sa.Column("confidence", sa.String(length=16), nullable=False, server_default="0.93"))
    op.add_column("private_photo_assets", sa.Column("auto_action", sa.String(length=24), nullable=False, server_default="approve"))
    op.add_column("private_photo_assets", sa.Column("revenue_state", sa.String(length=24), nullable=False, server_default="eligible"))
    op.add_column("private_photo_assets", sa.Column("user_visible_message", sa.Text(), nullable=False, server_default=""))
    op.add_column("private_photo_assets", sa.Column("manual_review", sa.Text(), nullable=True))
    op.add_column("private_photo_assets", sa.Column("appeal_state", sa.String(length=120), nullable=True))
    op.add_column("private_photo_assets", sa.Column("report_count", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("private_photo_assets", sa.Column("assigned_admin_id", sa.String(length=80), nullable=True))
    op.add_column("private_photo_assets", sa.Column("audit_refs", sa.Text(), nullable=False, server_default=""))
    op.add_column("private_photo_assets", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True))
    op.create_unique_constraint("uq_private_photo_assets_client_upload_id", "private_photo_assets", ["client_upload_id"])


def downgrade() -> None:
    op.drop_constraint("uq_private_photo_assets_client_upload_id", "private_photo_assets", type_="unique")
    op.drop_column("private_photo_assets", "updated_at")
    op.drop_column("private_photo_assets", "audit_refs")
    op.drop_column("private_photo_assets", "assigned_admin_id")
    op.drop_column("private_photo_assets", "report_count")
    op.drop_column("private_photo_assets", "appeal_state")
    op.drop_column("private_photo_assets", "manual_review")
    op.drop_column("private_photo_assets", "user_visible_message")
    op.drop_column("private_photo_assets", "revenue_state")
    op.drop_column("private_photo_assets", "auto_action")
    op.drop_column("private_photo_assets", "confidence")
    op.drop_column("private_photo_assets", "model_labels")
    op.drop_column("private_photo_assets", "risk_level")
    op.drop_column("private_photo_assets", "client_upload_id")
    op.drop_column("private_photo_assets", "upload_token")
    op.drop_column("private_photo_assets", "file_id")
