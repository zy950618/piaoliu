"""add core business schema

Revision ID: 0006_core_business_schema
Revises: 0005_plaza_comment_visibility
Create Date: 2026-06-24
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "0006_core_business_schema"
down_revision: str | None = "0005_plaza_comment_visibility"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("users", sa.Column("avatar_text", sa.String(length=8), nullable=True))
    op.add_column("users", sa.Column("avatar_url", sa.String(length=500), nullable=True))
    op.add_column("users", sa.Column("platform", sa.String(length=24), nullable=False, server_default="h5"))
    op.add_column("users", sa.Column("gender", sa.String(length=16), nullable=False, server_default="unknown"))
    op.add_column("users", sa.Column("city", sa.String(length=40), nullable=True))
    op.add_column("users", sa.Column("age_range", sa.String(length=24), nullable=True))
    op.add_column("users", sa.Column("is_vip", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("users", sa.Column("vip_level", sa.String(length=24), nullable=False, server_default="none"))
    op.add_column("users", sa.Column("drift_coins", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("users", sa.Column("face_verified", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("users", sa.Column("gender_verified", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("users", sa.Column("charm_value", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("users", sa.Column("status", sa.String(length=24), nullable=False, server_default="active"))

    op.add_column("plaza_comments", sa.Column("author_gender", sa.String(length=16), nullable=False, server_default="unknown"))
    op.add_column("plaza_comments", sa.Column("author_age_range", sa.String(length=24), nullable=True))
    op.add_column("plaza_comments", sa.Column("author_verified", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("plaza_comments", sa.Column("author_city", sa.String(length=40), nullable=True))

    op.create_table(
        "quota_balances",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("user_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("quota_type", sa.String(length=32), nullable=False),
        sa.Column("base", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("vip_bonus", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("ad_bonus", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("used", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("remaining", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("user_id", "quota_type", name="uq_quota_balances_user_type"),
    )
    op.create_index("ix_quota_balances_user_id", "quota_balances", ["user_id"])

    op.create_table(
        "checkin_records",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("user_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("checkin_date", sa.String(length=10), nullable=False),
        sa.Column("reward_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("streak_days", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("user_id", "checkin_date", name="uq_checkin_records_user_date"),
    )
    op.create_index("ix_checkin_records_user_id", "checkin_records", ["user_id"])

    op.create_table(
        "ad_reward_sessions",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("user_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("reward_per_quota", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("reward_coin", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="prepared"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("settled_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_ad_reward_sessions_user_id", "ad_reward_sessions", ["user_id"])

    op.create_table(
        "wallet_accounts",
        sa.Column("user_id", sa.String(length=64), sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("recharge_coins", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("earned_coins", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("gift_coins", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("withdrawable_coins", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("frozen_coins", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("charm_value", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("withdraw_threshold_charm", sa.Integer(), nullable=False, server_default="1000"),
        sa.Column("charm_exchange_rate", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "coin_ledger",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("user_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("coin_bucket", sa.String(length=24), nullable=False),
        sa.Column("withdrawable", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("business_type", sa.String(length=40), nullable=True),
        sa.Column("business_id", sa.String(length=80), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_coin_ledger_user_id", "coin_ledger", ["user_id"])

    op.create_table(
        "gift_products",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("price_coins", sa.Integer(), nullable=False),
        sa.Column("icon_text", sa.String(length=16), nullable=False),
        sa.Column("category", sa.String(length=40), nullable=True),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="active"),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )
    gift_products = sa.table(
        "gift_products",
        sa.column("id", sa.String),
        sa.column("name", sa.String),
        sa.column("price_coins", sa.Integer),
        sa.column("icon_text", sa.String),
        sa.column("category", sa.String),
        sa.column("status", sa.String),
        sa.column("sort_order", sa.Integer),
    )
    op.bulk_insert(
        gift_products,
        [
            {"id": "gift_shell", "name": "贝壳", "price_coins": 10, "icon_text": "贝", "category": "心意", "status": "active", "sort_order": 10},
            {"id": "gift_star", "name": "星光", "price_coins": 30, "icon_text": "星", "category": "心意", "status": "active", "sort_order": 20},
            {"id": "gift_flower", "name": "海花", "price_coins": 52, "icon_text": "花", "category": "浪漫", "status": "active", "sort_order": 30},
            {"id": "gift_bottle", "name": "玻璃瓶", "price_coins": 68, "icon_text": "瓶", "category": "漂流", "status": "active", "sort_order": 40},
            {"id": "gift_moon", "name": "月亮灯", "price_coins": 99, "icon_text": "月", "category": "浪漫", "status": "active", "sort_order": 50},
            {"id": "gift_whale", "name": "小鲸鱼", "price_coins": 188, "icon_text": "鲸", "category": "珍藏", "status": "active", "sort_order": 60},
            {"id": "gift_island", "name": "私人小岛", "price_coins": 520, "icon_text": "岛", "category": "珍藏", "status": "active", "sort_order": 70},
            {"id": "gift_crown", "name": "星海皇冠", "price_coins": 999, "icon_text": "冠", "category": "高级", "status": "active", "sort_order": 80},
        ],
    )

    op.create_table(
        "gift_orders",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("gift_id", sa.String(length=64), sa.ForeignKey("gift_products.id"), nullable=False),
        sa.Column("sender_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("receiver_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("source_type", sa.String(length=40), nullable=False, server_default="chat"),
        sa.Column("source_id", sa.String(length=80), nullable=True),
        sa.Column("price_coins", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="sent"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_gift_orders_gift_id", "gift_orders", ["gift_id"])
    op.create_index("ix_gift_orders_sender_id", "gift_orders", ["sender_id"])
    op.create_index("ix_gift_orders_receiver_id", "gift_orders", ["receiver_id"])

    op.create_table(
        "payment_orders",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("user_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("channel", sa.String(length=24), nullable=False),
        sa.Column("amount_coins", sa.Integer(), nullable=False),
        sa.Column("amount_cents", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="created"),
        sa.Column("prepay_id", sa.String(length=120), nullable=True),
        sa.Column("transaction_id", sa.String(length=120), nullable=True),
        sa.Column("callback_payload", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_payment_orders_user_id", "payment_orders", ["user_id"])

    op.create_table(
        "verification_profiles",
        sa.Column("user_id", sa.String(length=64), sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("face_verified", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("gender_verified", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("detected_gender", sa.String(length=16), nullable=False, server_default="unknown"),
        sa.Column("liveness_passed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("manual_review_status", sa.String(length=24), nullable=False, server_default="not_submitted"),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "referral_accounts",
        sa.Column("user_id", sa.String(length=64), sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("invite_code", sa.String(length=40), nullable=False, unique=True),
        sa.Column("invited_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("reward_vip_days", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("next_reward_need", sa.Integer(), nullable=False, server_default="0"),
    )

    op.create_table(
        "blacklist_entries",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("owner_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("blocked_user_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("nickname", sa.String(length=80), nullable=False),
        sa.Column("reason", sa.String(length=160), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="blocked"),
        sa.Column("blocked_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("owner_id", "blocked_user_id", name="uq_blacklist_owner_blocked"),
    )
    op.create_index("ix_blacklist_entries_owner_id", "blacklist_entries", ["owner_id"])
    op.create_index("ix_blacklist_entries_blocked_user_id", "blacklist_entries", ["blocked_user_id"])

    op.create_table(
        "conversation_threads",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("bottle_id", sa.String(length=64), nullable=True),
        sa.Column("user_a_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("user_b_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("participant_name", sa.String(length=80), nullable=False),
        sa.Column("participant_tag", sa.String(length=80), nullable=False),
        sa.Column("bottle_preview", sa.String(length=180), nullable=True),
        sa.Column("last_message", sa.String(length=180), nullable=True),
        sa.Column("unread_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_conversation_threads_bottle_id", "conversation_threads", ["bottle_id"])
    op.create_index("ix_conversation_threads_user_a_id", "conversation_threads", ["user_a_id"])
    op.create_index("ix_conversation_threads_user_b_id", "conversation_threads", ["user_b_id"])

    op.create_table(
        "game_rooms",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("owner_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("thread_id", sa.String(length=64), sa.ForeignKey("conversation_threads.id"), nullable=True),
        sa.Column("mode", sa.String(length=24), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="open"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_game_rooms_owner_id", "game_rooms", ["owner_id"])
    op.create_index("ix_game_rooms_thread_id", "game_rooms", ["thread_id"])

    op.create_table(
        "conversation_turns",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("thread_id", sa.String(length=64), sa.ForeignKey("conversation_threads.id"), nullable=False),
        sa.Column("sender_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("sender_name", sa.String(length=80), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("turn_type", sa.String(length=24), nullable=False, server_default="text"),
        sa.Column("media_url", sa.String(length=500), nullable=True),
        sa.Column("media_duration", sa.Integer(), nullable=True),
        sa.Column("flash_viewed", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("gift_id", sa.String(length=64), nullable=True),
        sa.Column("game_room_id", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_conversation_turns_thread_id", "conversation_turns", ["thread_id"])
    op.create_index("ix_conversation_turns_sender_id", "conversation_turns", ["sender_id"])

    op.create_table(
        "treehole_posts",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("author_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("author_name", sa.String(length=80), nullable=False),
        sa.Column("author_avatar_text", sa.String(length=8), nullable=True),
        sa.Column("author_avatar_url", sa.String(length=500), nullable=True),
        sa.Column("author_gender", sa.String(length=16), nullable=False, server_default="unknown"),
        sa.Column("author_age_range", sa.String(length=24), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("resonance_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("reply_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("paid_photo_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="approved"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_treehole_posts_author_id", "treehole_posts", ["author_id"])

    op.create_table(
        "treehole_replies",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("post_id", sa.String(length=64), sa.ForeignKey("treehole_posts.id"), nullable=False),
        sa.Column("author_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="approved"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_treehole_replies_post_id", "treehole_replies", ["post_id"])
    op.create_index("ix_treehole_replies_author_id", "treehole_replies", ["author_id"])

    op.create_table(
        "treehole_reactions",
        sa.Column("id", sa.String(length=64), primary_key=True),
        sa.Column("post_id", sa.String(length=64), sa.ForeignKey("treehole_posts.id"), nullable=False),
        sa.Column("user_id", sa.String(length=64), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("reaction_type", sa.String(length=24), nullable=False, server_default="resonate"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("post_id", "user_id", "reaction_type", name="uq_treehole_reactions_post_user_type"),
    )
    op.create_index("ix_treehole_reactions_post_id", "treehole_reactions", ["post_id"])
    op.create_index("ix_treehole_reactions_user_id", "treehole_reactions", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_treehole_reactions_user_id", table_name="treehole_reactions")
    op.drop_index("ix_treehole_reactions_post_id", table_name="treehole_reactions")
    op.drop_table("treehole_reactions")
    op.drop_index("ix_treehole_replies_author_id", table_name="treehole_replies")
    op.drop_index("ix_treehole_replies_post_id", table_name="treehole_replies")
    op.drop_table("treehole_replies")
    op.drop_index("ix_treehole_posts_author_id", table_name="treehole_posts")
    op.drop_table("treehole_posts")
    op.drop_index("ix_conversation_turns_sender_id", table_name="conversation_turns")
    op.drop_index("ix_conversation_turns_thread_id", table_name="conversation_turns")
    op.drop_table("conversation_turns")
    op.drop_index("ix_game_rooms_thread_id", table_name="game_rooms")
    op.drop_index("ix_game_rooms_owner_id", table_name="game_rooms")
    op.drop_table("game_rooms")
    op.drop_index("ix_conversation_threads_user_b_id", table_name="conversation_threads")
    op.drop_index("ix_conversation_threads_user_a_id", table_name="conversation_threads")
    op.drop_index("ix_conversation_threads_bottle_id", table_name="conversation_threads")
    op.drop_table("conversation_threads")
    op.drop_index("ix_blacklist_entries_blocked_user_id", table_name="blacklist_entries")
    op.drop_index("ix_blacklist_entries_owner_id", table_name="blacklist_entries")
    op.drop_table("blacklist_entries")
    op.drop_table("referral_accounts")
    op.drop_table("verification_profiles")
    op.drop_index("ix_payment_orders_user_id", table_name="payment_orders")
    op.drop_table("payment_orders")
    op.drop_index("ix_gift_orders_receiver_id", table_name="gift_orders")
    op.drop_index("ix_gift_orders_sender_id", table_name="gift_orders")
    op.drop_index("ix_gift_orders_gift_id", table_name="gift_orders")
    op.drop_table("gift_orders")
    op.drop_table("gift_products")
    op.drop_index("ix_coin_ledger_user_id", table_name="coin_ledger")
    op.drop_table("coin_ledger")
    op.drop_table("wallet_accounts")
    op.drop_index("ix_ad_reward_sessions_user_id", table_name="ad_reward_sessions")
    op.drop_table("ad_reward_sessions")
    op.drop_index("ix_checkin_records_user_id", table_name="checkin_records")
    op.drop_table("checkin_records")
    op.drop_index("ix_quota_balances_user_id", table_name="quota_balances")
    op.drop_table("quota_balances")

    op.drop_column("plaza_comments", "author_city")
    op.drop_column("plaza_comments", "author_verified")
    op.drop_column("plaza_comments", "author_age_range")
    op.drop_column("plaza_comments", "author_gender")

    op.drop_column("users", "status")
    op.drop_column("users", "charm_value")
    op.drop_column("users", "gender_verified")
    op.drop_column("users", "face_verified")
    op.drop_column("users", "drift_coins")
    op.drop_column("users", "vip_level")
    op.drop_column("users", "is_vip")
    op.drop_column("users", "age_range")
    op.drop_column("users", "city")
    op.drop_column("users", "gender")
    op.drop_column("users", "platform")
    op.drop_column("users", "avatar_url")
    op.drop_column("users", "avatar_text")
