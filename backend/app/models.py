from datetime import UTC, datetime

try:
    from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
    from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


    class Base(DeclarativeBase):
        pass


    class User(Base):
        __tablename__ = "users"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        nickname: Mapped[str] = mapped_column(String(80), nullable=False)
        role: Mapped[str] = mapped_column(String(32), nullable=False, default="user")
        avatar_text: Mapped[str | None] = mapped_column(String(8), nullable=True)
        avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
        platform: Mapped[str] = mapped_column(String(24), nullable=False, default="h5")
        gender: Mapped[str] = mapped_column(String(16), nullable=False, default="unknown")
        city: Mapped[str | None] = mapped_column(String(40), nullable=True)
        age_range: Mapped[str | None] = mapped_column(String(24), nullable=True)
        is_vip: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
        vip_level: Mapped[str] = mapped_column(String(24), nullable=False, default="none")
        drift_coins: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        face_verified: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
        gender_verified: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
        charm_value: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="active")
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class AdminUserRestriction(Base):
        __tablename__ = "admin_user_restrictions"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        status: Mapped[str] = mapped_column(String(24), nullable=False)
        reason: Mapped[str | None] = mapped_column(String(200), nullable=True)
        blocked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
        action_by: Mapped[str | None] = mapped_column(String(80), nullable=True)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
        updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class AdminAuditLog(Base):
        __tablename__ = "admin_audit_logs"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        actor: Mapped[str] = mapped_column(String(80), nullable=False)
        action: Mapped[str] = mapped_column(String(80), nullable=False)
        target_type: Mapped[str] = mapped_column(String(80), nullable=False)
        target_id: Mapped[str] = mapped_column(String(120), nullable=False)
        detail: Mapped[str | None] = mapped_column(Text, nullable=True)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class AppConfig(Base):
        __tablename__ = "app_configs"

        key: Mapped[str] = mapped_column(String(80), primary_key=True)
        value: Mapped[str] = mapped_column(Text, nullable=False)
        updated_by: Mapped[str | None] = mapped_column(String(80), nullable=True)
        updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class Bottle(Base):
        __tablename__ = "bottles"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        author_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        author_name: Mapped[str] = mapped_column(String(80), nullable=False)
        author_avatar_text: Mapped[str | None] = mapped_column(String(8), nullable=True)
        author_vip: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
        author_gender: Mapped[str] = mapped_column(String(16), nullable=False, default="unknown")
        author_age_range: Mapped[str | None] = mapped_column(String(24), nullable=True)
        author_city: Mapped[str | None] = mapped_column(String(40), nullable=True)
        author_verified: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
        content: Mapped[str] = mapped_column(Text, nullable=False)
        mood: Mapped[str] = mapped_column(String(32), nullable=False)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="pending")
        replies: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        target_gender: Mapped[str] = mapped_column(String(16), nullable=False, default="all")
        target_scope: Mapped[str] = mapped_column(String(24), nullable=False, default="all")
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class BottleReply(Base):
        __tablename__ = "bottle_replies"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        bottle_id: Mapped[str] = mapped_column(String(64), ForeignKey("bottles.id"), nullable=False, index=True)
        author_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        content: Mapped[str] = mapped_column(Text, nullable=False)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="pending")
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class Follow(Base):
        __tablename__ = "follows"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        follower_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        target_user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class PlazaPost(Base):
        __tablename__ = "plaza_posts"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        author_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        author_name: Mapped[str] = mapped_column(String(80), nullable=False)
        icon_text: Mapped[str] = mapped_column(String(8), nullable=False)
        topic: Mapped[str] = mapped_column(String(40), nullable=False)
        content: Mapped[str] = mapped_column(Text, nullable=False)
        media_type: Mapped[str] = mapped_column(String(16), nullable=False, default="text")
        media_count: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        gender: Mapped[str] = mapped_column(String(16), nullable=False, default="unknown")
        verified: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
        city: Mapped[str | None] = mapped_column(String(40), nullable=True, index=True)
        age_range: Mapped[str | None] = mapped_column(String(24), nullable=True, index=True)
        view_count: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        like_count: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        comment_count: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        comment_preview: Mapped[str | None] = mapped_column(String(160), nullable=True)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="approved")
        distance_text: Mapped[str | None] = mapped_column(String(40), nullable=True)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class PlazaMedia(Base):
        __tablename__ = "plaza_media"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        post_id: Mapped[str] = mapped_column(String(64), ForeignKey("plaza_posts.id"), nullable=False, index=True)
        owner_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        media_type: Mapped[str] = mapped_column(String(16), nullable=False)
        url: Mapped[str] = mapped_column(String(500), nullable=False)
        storage_key: Mapped[str] = mapped_column(String(240), nullable=False)
        mime_type: Mapped[str] = mapped_column(String(120), nullable=False)
        size_bytes: Mapped[int | None] = mapped_column(Integer(), nullable=True)
        duration_seconds: Mapped[int | None] = mapped_column(Integer(), nullable=True)
        width: Mapped[int | None] = mapped_column(Integer(), nullable=True)
        height: Mapped[int | None] = mapped_column(Integer(), nullable=True)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="pending")
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class PlazaComment(Base):
        __tablename__ = "plaza_comments"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        post_id: Mapped[str] = mapped_column(String(64), ForeignKey("plaza_posts.id"), nullable=False, index=True)
        author_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        author_name: Mapped[str] = mapped_column(String(80), nullable=False)
        icon_text: Mapped[str] = mapped_column(String(8), nullable=False)
        author_gender: Mapped[str] = mapped_column(String(16), nullable=False, default="unknown")
        author_age_range: Mapped[str | None] = mapped_column(String(24), nullable=True)
        author_verified: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
        author_city: Mapped[str | None] = mapped_column(String(40), nullable=True)
        content: Mapped[str] = mapped_column(Text, nullable=False)
        hidden_for_owner_only: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="approved")
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class PlazaLike(Base):
        __tablename__ = "plaza_likes"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        post_id: Mapped[str] = mapped_column(String(64), ForeignKey("plaza_posts.id"), nullable=False, index=True)
        user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class QuotaBalance(Base):
        __tablename__ = "quota_balances"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        quota_type: Mapped[str] = mapped_column(String(32), nullable=False)
        base: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        vip_bonus: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        ad_bonus: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        used: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        remaining: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
        __table_args__ = (UniqueConstraint("user_id", "quota_type", name="uq_quota_balances_user_type"),)


    class CheckinRecord(Base):
        __tablename__ = "checkin_records"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        checkin_date: Mapped[str] = mapped_column(String(10), nullable=False)
        reward_count: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        streak_days: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
        __table_args__ = (UniqueConstraint("user_id", "checkin_date", name="uq_checkin_records_user_date"),)


    class AdRewardSession(Base):
        __tablename__ = "ad_reward_sessions"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        reward_per_quota: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        reward_coin: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="prepared")
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
        settled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


    class WalletAccount(Base):
        __tablename__ = "wallet_accounts"

        user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), primary_key=True)
        recharge_coins: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        earned_coins: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        gift_coins: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        withdrawable_coins: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        frozen_coins: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        charm_value: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        withdraw_threshold_charm: Mapped[int] = mapped_column(Integer(), nullable=False, default=1000)
        charm_exchange_rate: Mapped[int] = mapped_column(Integer(), nullable=False, default=100)
        updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class CoinLedger(Base):
        __tablename__ = "coin_ledger"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        title: Mapped[str] = mapped_column(String(160), nullable=False)
        amount: Mapped[int] = mapped_column(Integer(), nullable=False)
        coin_bucket: Mapped[str] = mapped_column(String(24), nullable=False)
        withdrawable: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
        business_type: Mapped[str | None] = mapped_column(String(40), nullable=True)
        business_id: Mapped[str | None] = mapped_column(String(80), nullable=True)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class UserActivityRecord(Base):
        __tablename__ = "user_activity_records"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        record_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
        title: Mapped[str] = mapped_column(String(80), nullable=False)
        content: Mapped[str] = mapped_column(Text, nullable=False)
        visibility: Mapped[str | None] = mapped_column(String(40), nullable=True)
        source_type: Mapped[str | None] = mapped_column(String(40), nullable=True)
        source_id: Mapped[str | None] = mapped_column(String(80), nullable=True)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class PromptTemplate(Base):
        __tablename__ = "prompt_templates"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        prompt_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
        mode: Mapped[str | None] = mapped_column(String(40), nullable=True, index=True)
        category: Mapped[str] = mapped_column(String(40), nullable=False)
        text: Mapped[str] = mapped_column(Text, nullable=False)
        meaning: Mapped[str | None] = mapped_column(Text, nullable=True)
        visibility: Mapped[str | None] = mapped_column(String(40), nullable=True)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="active")
        sort_order: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class GiftProduct(Base):
        __tablename__ = "gift_products"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        name: Mapped[str] = mapped_column(String(80), nullable=False)
        price_coins: Mapped[int] = mapped_column(Integer(), nullable=False)
        icon_text: Mapped[str] = mapped_column(String(16), nullable=False)
        category: Mapped[str | None] = mapped_column(String(40), nullable=True)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="active")
        sort_order: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class GiftOrder(Base):
        __tablename__ = "gift_orders"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        gift_id: Mapped[str] = mapped_column(String(64), ForeignKey("gift_products.id"), nullable=False, index=True)
        sender_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        receiver_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        source_type: Mapped[str] = mapped_column(String(40), nullable=False, default="chat")
        source_id: Mapped[str | None] = mapped_column(String(80), nullable=True)
        price_coins: Mapped[int] = mapped_column(Integer(), nullable=False)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="sent")
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class PrivatePhotoAsset(Base):
        __tablename__ = "private_photo_assets"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        owner_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        owner_name: Mapped[str] = mapped_column(String(80), nullable=False)
        title: Mapped[str] = mapped_column(String(120), nullable=False)
        cover_tone: Mapped[str] = mapped_column(String(24), nullable=False, default="mint")
        price_coins: Mapped[int] = mapped_column(Integer(), nullable=False)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="approved")
        purchased_by_user_ids: Mapped[str] = mapped_column(Text, nullable=False, default="")
        file_id: Mapped[str | None] = mapped_column(String(120), nullable=True)
        upload_token: Mapped[str | None] = mapped_column(String(120), nullable=True)
        client_upload_id: Mapped[str | None] = mapped_column(String(120), nullable=True, unique=True)
        risk_level: Mapped[str] = mapped_column(String(24), nullable=False, default="low_risk")
        model_labels: Mapped[str] = mapped_column(Text, nullable=False, default="")
        confidence: Mapped[str] = mapped_column(String(16), nullable=False, default="0.93")
        auto_action: Mapped[str] = mapped_column(String(24), nullable=False, default="approve")
        revenue_state: Mapped[str] = mapped_column(String(24), nullable=False, default="eligible")
        user_visible_message: Mapped[str] = mapped_column(Text, nullable=False, default="")
        manual_review: Mapped[str | None] = mapped_column(Text, nullable=True)
        appeal_state: Mapped[str | None] = mapped_column(String(120), nullable=True)
        report_count: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        assigned_admin_id: Mapped[str | None] = mapped_column(String(80), nullable=True)
        audit_refs: Mapped[str] = mapped_column(Text, nullable=False, default="")
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
        updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class PaymentOrder(Base):
        __tablename__ = "payment_orders"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        channel: Mapped[str] = mapped_column(String(24), nullable=False)
        amount_coins: Mapped[int] = mapped_column(Integer(), nullable=False)
        amount_cents: Mapped[int] = mapped_column(Integer(), nullable=False)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="created")
        prepay_id: Mapped[str | None] = mapped_column(String(120), nullable=True)
        transaction_id: Mapped[str | None] = mapped_column(String(120), nullable=True)
        callback_payload: Mapped[str | None] = mapped_column(Text, nullable=True)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
        paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


    class MembershipOrder(Base):
        __tablename__ = "membership_orders"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        platform: Mapped[str] = mapped_column(String(24), nullable=False)
        product_id: Mapped[str] = mapped_column(String(64), nullable=False)
        transaction_id: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
        status: Mapped[str] = mapped_column(String(32), nullable=False, default="mock_verified")
        vip_level: Mapped[str] = mapped_column(String(24), nullable=False)
        verified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class MembershipProductConfig(Base):
        __tablename__ = "membership_product_configs"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        name: Mapped[str] = mapped_column(String(80), nullable=False)
        price_label: Mapped[str] = mapped_column(String(40), nullable=False)
        platform: Mapped[str] = mapped_column(String(24), nullable=False, default="all")
        benefits_text: Mapped[str] = mapped_column(Text, nullable=False)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="active")
        sort_order: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class VerificationProfile(Base):
        __tablename__ = "verification_profiles"

        user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), primary_key=True)
        face_verified: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
        gender_verified: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
        detected_gender: Mapped[str] = mapped_column(String(16), nullable=False, default="unknown")
        liveness_passed: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
        manual_review_status: Mapped[str] = mapped_column(String(24), nullable=False, default="not_submitted")
        submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
        reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


    class ReferralAccount(Base):
        __tablename__ = "referral_accounts"

        user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), primary_key=True)
        invite_code: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
        invited_count: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        reward_vip_days: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        next_reward_need: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)


    class BlacklistEntry(Base):
        __tablename__ = "blacklist_entries"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        owner_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        blocked_user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        nickname: Mapped[str] = mapped_column(String(80), nullable=False)
        reason: Mapped[str] = mapped_column(String(160), nullable=False)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="blocked")
        blocked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
        __table_args__ = (UniqueConstraint("owner_id", "blocked_user_id", name="uq_blacklist_owner_blocked"),)


    class ContentReport(Base):
        __tablename__ = "content_reports"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        reporter_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        target_type: Mapped[str] = mapped_column(String(32), nullable=False)
        target_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
        reason: Mapped[str] = mapped_column(String(160), nullable=False)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="queued")
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
        __table_args__ = (UniqueConstraint("reporter_id", "target_type", "target_id", "reason", name="uq_content_reports_once"),)


    class FriendRequest(Base):
        __tablename__ = "friend_requests"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        requester_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        target_user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="requested")
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
        __table_args__ = (UniqueConstraint("requester_id", "target_user_id", name="uq_friend_requests_pair"),)


    class MessageNotification(Base):
        __tablename__ = "message_notifications"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        title: Mapped[str] = mapped_column(String(120), nullable=False)
        body: Mapped[str] = mapped_column(String(500), nullable=False)
        unread: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)
        business_type: Mapped[str | None] = mapped_column(String(40), nullable=True)
        business_id: Mapped[str | None] = mapped_column(String(80), nullable=True)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class ChatAppeal(Base):
        __tablename__ = "chat_appeals"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        thread_id: Mapped[str] = mapped_column(String(64), ForeignKey("conversation_threads.id"), nullable=False, index=True)
        user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        reason: Mapped[str] = mapped_column(String(240), nullable=False)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="pending", index=True)
        admin_reason: Mapped[str | None] = mapped_column(String(240), nullable=True)
        audit_refs: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
        updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
        __table_args__ = (UniqueConstraint("thread_id", "user_id", "status", name="uq_chat_appeals_open_once"),)


    class ConversationThread(Base):
        __tablename__ = "conversation_threads"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        bottle_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
        user_a_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        user_b_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        participant_name: Mapped[str] = mapped_column(String(80), nullable=False)
        participant_tag: Mapped[str] = mapped_column(String(80), nullable=False)
        bottle_preview: Mapped[str | None] = mapped_column(String(180), nullable=True)
        last_message: Mapped[str | None] = mapped_column(String(180), nullable=True)
        unread_count: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="active")
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
        updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class ConversationTurn(Base):
        __tablename__ = "conversation_turns"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        thread_id: Mapped[str] = mapped_column(String(64), ForeignKey("conversation_threads.id"), nullable=False, index=True)
        sender_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        sender_name: Mapped[str] = mapped_column(String(80), nullable=False)
        body: Mapped[str] = mapped_column(Text, nullable=False)
        turn_type: Mapped[str] = mapped_column(String(24), nullable=False, default="text")
        media_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
        media_duration: Mapped[int | None] = mapped_column(Integer(), nullable=True)
        flash_viewed: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
        gift_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
        game_room_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class GameRoom(Base):
        __tablename__ = "game_rooms"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        owner_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        thread_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("conversation_threads.id"), nullable=True, index=True)
        mode: Mapped[str] = mapped_column(String(24), nullable=False)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="open")
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class ChatContextRequestRecord(Base):
        __tablename__ = "chat_context_requests"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        initiator_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
        target_user_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
        source_type: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
        source_id: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
        source_title: Mapped[str | None] = mapped_column(String(120), nullable=True)
        reply_id: Mapped[str | None] = mapped_column(String(120), nullable=True)
        initiator_action: Mapped[str] = mapped_column(String(40), nullable=False)
        evidence_id: Mapped[str | None] = mapped_column(String(120), nullable=True)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="pending", index=True)
        conversation_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
        confirm_action: Mapped[str | None] = mapped_column(String(40), nullable=True)
        confirm_evidence_id: Mapped[str | None] = mapped_column(String(120), nullable=True)
        reject_reason: Mapped[str | None] = mapped_column(String(160), nullable=True)
        audit_refs: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
        updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class ChatConversationRecord(Base):
        __tablename__ = "chat_conversations"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="active", index=True)
        source_type: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
        source_id: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
        source_title: Mapped[str | None] = mapped_column(String(120), nullable=True)
        participant_a_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
        participant_b_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
        friendship_state: Mapped[str] = mapped_column(String(24), nullable=False, default="none")
        expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
        last_message: Mapped[str | None] = mapped_column(String(500), nullable=True)
        risk_state: Mapped[str] = mapped_column(String(24), nullable=False, default="clear")
        report_state: Mapped[str] = mapped_column(String(24), nullable=False, default="none")
        audit_refs: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
        updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class ChatMessageRecord(Base):
        __tablename__ = "chat_messages"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        conversation_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
        sender_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
        content_type: Mapped[str] = mapped_column(String(32), nullable=False, default="text")
        content: Mapped[str] = mapped_column(Text, nullable=False)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="sent")
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class ChatConversationReportRecord(Base):
        __tablename__ = "chat_conversation_reports"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        conversation_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
        reporter_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
        reason: Mapped[str] = mapped_column(String(160), nullable=False)
        message_ids: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
        description: Mapped[str | None] = mapped_column(Text, nullable=True)
        audit_id: Mapped[str] = mapped_column(String(64), nullable=False)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class ChatConversationBlockRecord(Base):
        __tablename__ = "chat_conversation_blocks"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        conversation_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
        blocker_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
        blocked_user_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
        reason: Mapped[str | None] = mapped_column(String(160), nullable=True)
        audit_id: Mapped[str] = mapped_column(String(64), nullable=False)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
        __table_args__ = (UniqueConstraint("blocker_id", "blocked_user_id", name="uq_chat_blocks_pair"),)


    class TreeholePost(Base):
        __tablename__ = "treehole_posts"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        author_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        author_name: Mapped[str] = mapped_column(String(80), nullable=False)
        author_avatar_text: Mapped[str | None] = mapped_column(String(8), nullable=True)
        author_avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
        author_gender: Mapped[str] = mapped_column(String(16), nullable=False, default="unknown")
        author_age_range: Mapped[str | None] = mapped_column(String(24), nullable=True)
        content: Mapped[str] = mapped_column(Text, nullable=False)
        resonance_count: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        reply_count: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        paid_photo_count: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="approved")
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class TreeholeReply(Base):
        __tablename__ = "treehole_replies"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        post_id: Mapped[str] = mapped_column(String(64), ForeignKey("treehole_posts.id"), nullable=False, index=True)
        author_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        content: Mapped[str] = mapped_column(Text, nullable=False)
        status: Mapped[str] = mapped_column(String(24), nullable=False, default="approved")
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class TreeholeReaction(Base):
        __tablename__ = "treehole_reactions"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        post_id: Mapped[str] = mapped_column(String(64), ForeignKey("treehole_posts.id"), nullable=False, index=True)
        user_id: Mapped[str] = mapped_column(String(64), ForeignKey("users.id"), nullable=False, index=True)
        reaction_type: Mapped[str] = mapped_column(String(24), nullable=False, default="resonate")
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))
        __table_args__ = (UniqueConstraint("post_id", "user_id", "reaction_type", name="uq_treehole_reactions_post_user_type"),)
except ModuleNotFoundError:
    class _FallbackMetadata:
        def __init__(self) -> None:
            self.tables: dict[str, object] = {}

    class Base:
        metadata = _FallbackMetadata()

    class User:
        __tablename__ = "users"

    class AdminAuditLog:
        __tablename__ = "admin_audit_logs"

    class AppConfig:
        __tablename__ = "app_configs"

    class Bottle:
        __tablename__ = "bottles"

    class BottleReply:
        __tablename__ = "bottle_replies"

    class Follow:
        __tablename__ = "follows"

    class PlazaPost:
        __tablename__ = "plaza_posts"

    class PlazaMedia:
        __tablename__ = "plaza_media"

    class PlazaComment:
        __tablename__ = "plaza_comments"

    class PlazaLike:
        __tablename__ = "plaza_likes"

    class QuotaBalance:
        __tablename__ = "quota_balances"

    class CheckinRecord:
        __tablename__ = "checkin_records"

    class AdRewardSession:
        __tablename__ = "ad_reward_sessions"

    class WalletAccount:
        __tablename__ = "wallet_accounts"

    class CoinLedger:
        __tablename__ = "coin_ledger"

    class UserActivityRecord:
        __tablename__ = "user_activity_records"

    class PromptTemplate:
        __tablename__ = "prompt_templates"

    class GiftProduct:
        __tablename__ = "gift_products"

    class GiftOrder:
        __tablename__ = "gift_orders"

    class PaymentOrder:
        __tablename__ = "payment_orders"

    class MembershipOrder:
        __tablename__ = "membership_orders"

    class MembershipProductConfig:
        __tablename__ = "membership_product_configs"

    class PrivatePhotoAsset:
        __tablename__ = "private_photo_assets"

    class AdminUserRestriction:
        __tablename__ = "admin_user_restrictions"

    class VerificationProfile:
        __tablename__ = "verification_profiles"

    class ReferralAccount:
        __tablename__ = "referral_accounts"

    class BlacklistEntry:
        __tablename__ = "blacklist_entries"

    class ContentReport:
        __tablename__ = "content_reports"

    class FriendRequest:
        __tablename__ = "friend_requests"

    class MessageNotification:
        __tablename__ = "message_notifications"

    class ChatAppeal:
        __tablename__ = "chat_appeals"

    class ConversationThread:
        __tablename__ = "conversation_threads"

    class ConversationTurn:
        __tablename__ = "conversation_turns"

    class GameRoom:
        __tablename__ = "game_rooms"

    class ChatContextRequestRecord:
        __tablename__ = "chat_context_requests"

    class ChatConversationRecord:
        __tablename__ = "chat_conversations"

    class ChatMessageRecord:
        __tablename__ = "chat_messages"

    class ChatConversationReportRecord:
        __tablename__ = "chat_conversation_reports"

    class ChatConversationBlockRecord:
        __tablename__ = "chat_conversation_blocks"

    class TreeholePost:
        __tablename__ = "treehole_posts"

    class TreeholeReply:
        __tablename__ = "treehole_replies"

    class TreeholeReaction:
        __tablename__ = "treehole_reactions"

    Base.metadata.tables[User.__tablename__] = User
    Base.metadata.tables[AdminAuditLog.__tablename__] = AdminAuditLog
    Base.metadata.tables[AppConfig.__tablename__] = AppConfig
    Base.metadata.tables[AdminUserRestriction.__tablename__] = AdminUserRestriction
    Base.metadata.tables[Bottle.__tablename__] = Bottle
    Base.metadata.tables[BottleReply.__tablename__] = BottleReply
    Base.metadata.tables[Follow.__tablename__] = Follow
    Base.metadata.tables[PlazaPost.__tablename__] = PlazaPost
    Base.metadata.tables[PlazaMedia.__tablename__] = PlazaMedia
    Base.metadata.tables[PlazaComment.__tablename__] = PlazaComment
    Base.metadata.tables[PlazaLike.__tablename__] = PlazaLike
    Base.metadata.tables[QuotaBalance.__tablename__] = QuotaBalance
    Base.metadata.tables[CheckinRecord.__tablename__] = CheckinRecord
    Base.metadata.tables[AdRewardSession.__tablename__] = AdRewardSession
    Base.metadata.tables[WalletAccount.__tablename__] = WalletAccount
    Base.metadata.tables[CoinLedger.__tablename__] = CoinLedger
    Base.metadata.tables[UserActivityRecord.__tablename__] = UserActivityRecord
    Base.metadata.tables[PromptTemplate.__tablename__] = PromptTemplate
    Base.metadata.tables[GiftProduct.__tablename__] = GiftProduct
    Base.metadata.tables[GiftOrder.__tablename__] = GiftOrder
    Base.metadata.tables[PaymentOrder.__tablename__] = PaymentOrder
    Base.metadata.tables[MembershipOrder.__tablename__] = MembershipOrder
    Base.metadata.tables[MembershipProductConfig.__tablename__] = MembershipProductConfig
    Base.metadata.tables[PrivatePhotoAsset.__tablename__] = PrivatePhotoAsset
    Base.metadata.tables[VerificationProfile.__tablename__] = VerificationProfile
    Base.metadata.tables[ReferralAccount.__tablename__] = ReferralAccount
    Base.metadata.tables[BlacklistEntry.__tablename__] = BlacklistEntry
    Base.metadata.tables[ContentReport.__tablename__] = ContentReport
    Base.metadata.tables[FriendRequest.__tablename__] = FriendRequest
    Base.metadata.tables[MessageNotification.__tablename__] = MessageNotification
    Base.metadata.tables[ChatAppeal.__tablename__] = ChatAppeal
    Base.metadata.tables[ConversationThread.__tablename__] = ConversationThread
    Base.metadata.tables[ConversationTurn.__tablename__] = ConversationTurn
    Base.metadata.tables[GameRoom.__tablename__] = GameRoom
    Base.metadata.tables[ChatContextRequestRecord.__tablename__] = ChatContextRequestRecord
    Base.metadata.tables[ChatConversationRecord.__tablename__] = ChatConversationRecord
    Base.metadata.tables[ChatMessageRecord.__tablename__] = ChatMessageRecord
    Base.metadata.tables[ChatConversationReportRecord.__tablename__] = ChatConversationReportRecord
    Base.metadata.tables[ChatConversationBlockRecord.__tablename__] = ChatConversationBlockRecord
    Base.metadata.tables[TreeholePost.__tablename__] = TreeholePost
    Base.metadata.tables[TreeholeReply.__tablename__] = TreeholeReply
    Base.metadata.tables[TreeholeReaction.__tablename__] = TreeholeReaction
