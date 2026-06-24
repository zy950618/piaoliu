"""replace bottle target city with target scope

Revision ID: 0003_bottle_target_scope
Revises: 0002_bottle_relation_models
Create Date: 2026-06-23
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "0003_bottle_target_scope"
down_revision: str | None = "0002_bottle_relation_models"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "bottles",
        sa.Column("target_scope", sa.String(length=24), nullable=False, server_default="all"),
    )
    op.execute(
        "UPDATE bottles SET target_scope = CASE "
        "WHEN target_city = '全国' THEN 'all' "
        "WHEN target_city IS NULL THEN 'all' "
        "ELSE 'same_city' END"
    )
    op.drop_column("bottles", "target_city")


def downgrade() -> None:
    op.add_column(
        "bottles",
        sa.Column("target_city", sa.String(length=40), nullable=False, server_default="全国"),
    )
    op.execute(
        "UPDATE bottles SET target_city = CASE "
        "WHEN target_scope = 'same_city' THEN author_city "
        "WHEN target_scope = 'nearby' THEN author_city "
        "ELSE '全国' END"
    )
    op.drop_column("bottles", "target_scope")
