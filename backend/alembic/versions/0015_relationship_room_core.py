"""relationship and room core

Revision ID: 0015_relationship_room_core
Revises: 0014_chat_appeals
"""

from alembic import op
import sqlalchemy as sa


revision = "0015_relationship_room_core"
down_revision = "0014_chat_appeals"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "interaction_receipts",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("actor_id", sa.String(64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("target_user_id", sa.String(64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("source_type", sa.String(40), nullable=False),
        sa.Column("source_id", sa.String(120), nullable=False),
        sa.Column("status", sa.String(24), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("actor_id", "target_user_id", "source_type", "source_id", name="uq_interaction_receipt_source"),
    )
    op.create_index("ix_interaction_actor", "interaction_receipts", ["actor_id"])
    op.create_index("ix_interaction_target", "interaction_receipts", ["target_user_id"])
    op.create_index("ix_interaction_source", "interaction_receipts", ["source_type", "source_id"])

    op.create_table(
        "chat_grants",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("user_a_id", sa.String(64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("user_b_id", sa.String(64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("source_type", sa.String(40), nullable=False),
        sa.Column("source_id", sa.String(120), nullable=True),
        sa.Column("status", sa.String(24), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("user_a_id", "user_b_id", "source_type", "source_id", name="uq_chat_grant_source"),
    )
    op.create_index("ix_chat_grants_a", "chat_grants", ["user_a_id"])
    op.create_index("ix_chat_grants_b", "chat_grants", ["user_b_id"])

    op.create_table(
        "friendships",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("user_a_id", sa.String(64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("user_b_id", sa.String(64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("status", sa.String(24), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("removed_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("user_a_id", "user_b_id", name="uq_friendship_pair"),
    )
    op.create_index("ix_friendships_a", "friendships", ["user_a_id"])
    op.create_index("ix_friendships_b", "friendships", ["user_b_id"])

    op.create_table(
        "conversation_user_states",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("conversation_id", sa.String(64), nullable=False),
        sa.Column("user_id", sa.String(64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("last_read_seq", sa.Integer(), nullable=False),
        sa.Column("history_cleared_before_seq", sa.Integer(), nullable=False),
        sa.Column("hidden_until_seq", sa.Integer(), nullable=False),
        sa.Column("muted", sa.Boolean(), nullable=False),
        sa.Column("cleanup_days", sa.Integer(), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("conversation_id", "user_id", name="uq_conversation_user_state"),
    )
    op.create_index("ix_conversation_state_conversation", "conversation_user_states", ["conversation_id"])
    op.create_index("ix_conversation_state_user", "conversation_user_states", ["user_id"])

    op.create_table(
        "rooms",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("owner_id", sa.String(64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("conversation_id", sa.String(64), nullable=True),
        sa.Column("name", sa.String(80), nullable=False),
        sa.Column("visibility", sa.String(24), nullable=False),
        sa.Column("size_mode", sa.String(24), nullable=False),
        sa.Column("join_policy", sa.String(24), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=False),
        sa.Column("allow_member_invite", sa.Boolean(), nullable=False),
        sa.Column("status", sa.String(24), nullable=False),
        sa.Column("last_active_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("dissolved_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_rooms_owner", "rooms", ["owner_id"])
    op.create_index("ix_rooms_visibility_status", "rooms", ["visibility", "status"])

    op.create_table(
        "room_members",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("room_id", sa.String(64), sa.ForeignKey("rooms.id"), nullable=False),
        sa.Column("user_id", sa.String(64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("role", sa.String(24), nullable=False),
        sa.Column("status", sa.String(24), nullable=False),
        sa.Column("cannot_rejoin", sa.Boolean(), nullable=False),
        sa.Column("joined_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("left_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("room_id", "user_id", name="uq_room_member"),
    )
    op.create_index("ix_room_members_room", "room_members", ["room_id"])
    op.create_index("ix_room_members_user", "room_members", ["user_id"])
    op.create_index("ix_room_members_status", "room_members", ["status"])

    op.create_table(
        "room_invitations",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("room_id", sa.String(64), sa.ForeignKey("rooms.id"), nullable=False),
        sa.Column("inviter_id", sa.String(64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("invitee_id", sa.String(64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("status", sa.String(24), nullable=False),
        sa.Column("idempotency_key", sa.String(120), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("room_id", "invitee_id", "status", name="uq_room_invitation_pending"),
        sa.UniqueConstraint("inviter_id", "idempotency_key", name="uq_room_invitation_idempotency"),
    )
    op.create_index("ix_room_invites_room", "room_invitations", ["room_id"])
    op.create_index("ix_room_invites_inviter", "room_invitations", ["inviter_id"])
    op.create_index("ix_room_invites_invitee", "room_invitations", ["invitee_id"])
    op.create_index("ix_room_invites_status", "room_invitations", ["status"])


def downgrade() -> None:
    op.drop_table("room_invitations")
    op.drop_table("room_members")
    op.drop_table("rooms")
    op.drop_table("conversation_user_states")
    op.drop_table("friendships")
    op.drop_table("chat_grants")
    op.drop_table("interaction_receipts")
