"""app config ad reward

Revision ID: 0013_app_configs_ad_reward
Revises: 0012_private_photo_reviews
Create Date: 2026-06-30 14:10:00
"""

from alembic import op
import sqlalchemy as sa

revision = "0013_app_configs_ad_reward"
down_revision = "0012_private_photo_reviews"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "app_configs",
        sa.Column("key", sa.String(length=80), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("updated_by", sa.String(length=80), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("key"),
    )


def downgrade() -> None:
    op.drop_table("app_configs")
