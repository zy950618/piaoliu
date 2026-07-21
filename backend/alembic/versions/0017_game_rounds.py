"""add server-authoritative game rounds

Revision ID: 0017_game_rounds
Revises: 0016_chat_realtime_sequence
Create Date: 2026-07-21
"""

from alembic import op
import sqlalchemy as sa


revision = "0017_game_rounds"
down_revision = "0016_chat_realtime_sequence"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "game_rounds",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("room_id", sa.String(64), sa.ForeignKey("rooms.id"), nullable=False),
        sa.Column("initiator_id", sa.String(64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("mode", sa.String(24), nullable=False),
        sa.Column("status", sa.String(24), nullable=False),
        sa.Column("prompt_id", sa.String(64), nullable=True),
        sa.Column("prompt_text", sa.Text(), nullable=True),
        sa.Column("result_json", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_game_rounds_room", "game_rounds", ["room_id"])
    op.create_index("ix_game_rounds_initiator", "game_rounds", ["initiator_id"])
    op.create_index("ix_game_rounds_mode_status", "game_rounds", ["mode", "status"])


def downgrade() -> None:
    op.drop_table("game_rounds")
