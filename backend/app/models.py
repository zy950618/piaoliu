from datetime import UTC, datetime

try:
    from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
    from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


    class Base(DeclarativeBase):
        pass


    class User(Base):
        __tablename__ = "users"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        nickname: Mapped[str] = mapped_column(String(80), nullable=False)
        role: Mapped[str] = mapped_column(String(32), nullable=False, default="user")
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


    class AdminAuditLog(Base):
        __tablename__ = "admin_audit_logs"

        id: Mapped[str] = mapped_column(String(64), primary_key=True)
        actor: Mapped[str] = mapped_column(String(80), nullable=False)
        action: Mapped[str] = mapped_column(String(80), nullable=False)
        target_type: Mapped[str] = mapped_column(String(80), nullable=False)
        target_id: Mapped[str] = mapped_column(String(120), nullable=False)
        detail: Mapped[str | None] = mapped_column(Text, nullable=True)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC))


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

    Base.metadata.tables[User.__tablename__] = User
    Base.metadata.tables[AdminAuditLog.__tablename__] = AdminAuditLog
    Base.metadata.tables[Bottle.__tablename__] = Bottle
    Base.metadata.tables[BottleReply.__tablename__] = BottleReply
    Base.metadata.tables[Follow.__tablename__] = Follow
    Base.metadata.tables[PlazaPost.__tablename__] = PlazaPost
    Base.metadata.tables[PlazaMedia.__tablename__] = PlazaMedia
    Base.metadata.tables[PlazaComment.__tablename__] = PlazaComment
    Base.metadata.tables[PlazaLike.__tablename__] = PlazaLike
