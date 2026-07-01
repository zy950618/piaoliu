"""context chat persistence

Revision ID: 0011_context_chat_persistence
Revises: 0010_membership_product_configs
Create Date: 2026-06-30
"""

from alembic import op
import sqlalchemy as sa


revision = "0011_context_chat_persistence"
down_revision = "0010_membership_product_configs"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "chat_context_requests",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("initiator_id", sa.String(length=64), nullable=False),
        sa.Column("target_user_id", sa.String(length=64), nullable=False),
        sa.Column("source_type", sa.String(length=40), nullable=False),
        sa.Column("source_id", sa.String(length=120), nullable=True),
        sa.Column("source_title", sa.String(length=120), nullable=True),
        sa.Column("reply_id", sa.String(length=120), nullable=True),
        sa.Column("initiator_action", sa.String(length=40), nullable=False),
        sa.Column("evidence_id", sa.String(length=120), nullable=True),
        sa.Column("status", sa.String(length=24), nullable=False),
        sa.Column("conversation_id", sa.String(length=64), nullable=True),
        sa.Column("confirm_action", sa.String(length=40), nullable=True),
        sa.Column("confirm_evidence_id", sa.String(length=120), nullable=True),
        sa.Column("reject_reason", sa.String(length=160), nullable=True),
        sa.Column("audit_refs", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_chat_context_requests_initiator_id", "chat_context_requests", ["initiator_id"])
    op.create_index("ix_chat_context_requests_target_user_id", "chat_context_requests", ["target_user_id"])
    op.create_index("ix_chat_context_requests_source_type", "chat_context_requests", ["source_type"])
    op.create_index("ix_chat_context_requests_source_id", "chat_context_requests", ["source_id"])
    op.create_index("ix_chat_context_requests_status", "chat_context_requests", ["status"])
    op.create_index("ix_chat_context_requests_conversation_id", "chat_context_requests", ["conversation_id"])

    op.create_table(
        "chat_conversations",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("status", sa.String(length=24), nullable=False),
        sa.Column("source_type", sa.String(length=40), nullable=False),
        sa.Column("source_id", sa.String(length=120), nullable=True),
        sa.Column("source_title", sa.String(length=120), nullable=True),
        sa.Column("participant_a_id", sa.String(length=64), nullable=False),
        sa.Column("participant_b_id", sa.String(length=64), nullable=False),
        sa.Column("friendship_state", sa.String(length=24), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("last_message", sa.String(length=500), nullable=True),
        sa.Column("risk_state", sa.String(length=24), nullable=False),
        sa.Column("report_state", sa.String(length=24), nullable=False),
        sa.Column("audit_refs", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_chat_conversations_status", "chat_conversations", ["status"])
    op.create_index("ix_chat_conversations_source_type", "chat_conversations", ["source_type"])
    op.create_index("ix_chat_conversations_source_id", "chat_conversations", ["source_id"])
    op.create_index("ix_chat_conversations_participant_a_id", "chat_conversations", ["participant_a_id"])
    op.create_index("ix_chat_conversations_participant_b_id", "chat_conversations", ["participant_b_id"])

    op.create_table(
        "chat_messages",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("conversation_id", sa.String(length=64), nullable=False),
        sa.Column("sender_id", sa.String(length=64), nullable=False),
        sa.Column("content_type", sa.String(length=32), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_chat_messages_conversation_id", "chat_messages", ["conversation_id"])
    op.create_index("ix_chat_messages_sender_id", "chat_messages", ["sender_id"])

    op.create_table(
        "chat_conversation_reports",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("conversation_id", sa.String(length=64), nullable=False),
        sa.Column("reporter_id", sa.String(length=64), nullable=False),
        sa.Column("reason", sa.String(length=160), nullable=False),
        sa.Column("message_ids", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("audit_id", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_chat_conversation_reports_conversation_id", "chat_conversation_reports", ["conversation_id"])
    op.create_index("ix_chat_conversation_reports_reporter_id", "chat_conversation_reports", ["reporter_id"])

    op.create_table(
        "chat_conversation_blocks",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("conversation_id", sa.String(length=64), nullable=False),
        sa.Column("blocker_id", sa.String(length=64), nullable=False),
        sa.Column("blocked_user_id", sa.String(length=64), nullable=False),
        sa.Column("reason", sa.String(length=160), nullable=True),
        sa.Column("audit_id", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("blocker_id", "blocked_user_id", name="uq_chat_blocks_pair"),
    )
    op.create_index("ix_chat_conversation_blocks_conversation_id", "chat_conversation_blocks", ["conversation_id"])
    op.create_index("ix_chat_conversation_blocks_blocker_id", "chat_conversation_blocks", ["blocker_id"])
    op.create_index("ix_chat_conversation_blocks_blocked_user_id", "chat_conversation_blocks", ["blocked_user_id"])


def downgrade() -> None:
    op.drop_index("ix_chat_conversation_blocks_blocked_user_id", table_name="chat_conversation_blocks")
    op.drop_index("ix_chat_conversation_blocks_blocker_id", table_name="chat_conversation_blocks")
    op.drop_index("ix_chat_conversation_blocks_conversation_id", table_name="chat_conversation_blocks")
    op.drop_table("chat_conversation_blocks")
    op.drop_index("ix_chat_conversation_reports_reporter_id", table_name="chat_conversation_reports")
    op.drop_index("ix_chat_conversation_reports_conversation_id", table_name="chat_conversation_reports")
    op.drop_table("chat_conversation_reports")
    op.drop_index("ix_chat_messages_sender_id", table_name="chat_messages")
    op.drop_index("ix_chat_messages_conversation_id", table_name="chat_messages")
    op.drop_table("chat_messages")
    op.drop_index("ix_chat_conversations_participant_b_id", table_name="chat_conversations")
    op.drop_index("ix_chat_conversations_participant_a_id", table_name="chat_conversations")
    op.drop_index("ix_chat_conversations_source_id", table_name="chat_conversations")
    op.drop_index("ix_chat_conversations_source_type", table_name="chat_conversations")
    op.drop_index("ix_chat_conversations_status", table_name="chat_conversations")
    op.drop_table("chat_conversations")
    op.drop_index("ix_chat_context_requests_conversation_id", table_name="chat_context_requests")
    op.drop_index("ix_chat_context_requests_status", table_name="chat_context_requests")
    op.drop_index("ix_chat_context_requests_source_id", table_name="chat_context_requests")
    op.drop_index("ix_chat_context_requests_source_type", table_name="chat_context_requests")
    op.drop_index("ix_chat_context_requests_target_user_id", table_name="chat_context_requests")
    op.drop_index("ix_chat_context_requests_initiator_id", table_name="chat_context_requests")
    op.drop_table("chat_context_requests")
