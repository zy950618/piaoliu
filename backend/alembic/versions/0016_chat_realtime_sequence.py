"""add reliable chat message sequencing

Revision ID: 0016_chat_realtime_sequence
Revises: 0015_relationship_room_core
Create Date: 2026-07-21
"""

from alembic import op
import sqlalchemy as sa


revision = "0016_chat_realtime_sequence"
down_revision = "0015_relationship_room_core"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "chat_conversations",
        sa.Column("next_message_sequence", sa.BigInteger(), nullable=False, server_default="1"),
    )
    op.add_column("chat_messages", sa.Column("client_message_id", sa.String(length=120), nullable=True))
    op.add_column("chat_messages", sa.Column("sequence", sa.BigInteger(), nullable=True))
    op.execute(
        """
        WITH ranked AS (
            SELECT id, ROW_NUMBER() OVER (
                PARTITION BY conversation_id ORDER BY created_at, id
            ) AS sequence
            FROM chat_messages
        )
        UPDATE chat_messages
        SET sequence = ranked.sequence
        FROM ranked
        WHERE chat_messages.id = ranked.id
        """
    )
    op.execute("UPDATE chat_messages SET client_message_id = id WHERE client_message_id IS NULL")
    op.execute(
        """
        UPDATE chat_conversations AS conversation
        SET next_message_sequence = COALESCE((
            SELECT MAX(message.sequence) + 1
            FROM chat_messages AS message
            WHERE message.conversation_id = conversation.id
        ), 1)
        """
    )
    op.alter_column("chat_messages", "sequence", nullable=False)
    op.create_unique_constraint(
        "uq_chat_message_sequence",
        "chat_messages",
        ["conversation_id", "sequence"],
    )
    op.create_unique_constraint(
        "uq_chat_message_client_id",
        "chat_messages",
        ["conversation_id", "sender_id", "client_message_id"],
    )
    op.create_index("ix_chat_messages_conversation_sequence", "chat_messages", ["conversation_id", "sequence"])


def downgrade() -> None:
    op.drop_index("ix_chat_messages_conversation_sequence", table_name="chat_messages")
    op.drop_constraint("uq_chat_message_client_id", "chat_messages", type_="unique")
    op.drop_constraint("uq_chat_message_sequence", "chat_messages", type_="unique")
    op.drop_column("chat_messages", "sequence")
    op.drop_column("chat_messages", "client_message_id")
    op.drop_column("chat_conversations", "next_message_sequence")
