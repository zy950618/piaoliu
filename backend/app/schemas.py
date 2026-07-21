from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field


class QuotaType(StrEnum):
    fish_bottle = "fish_bottle"
    throw_bottle = "throw_bottle"
    truth = "truth"
    dare = "dare"
    treehole_post = "treehole_post"


class ContentStatus(StrEnum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class UserProfile(BaseModel):
    id: str
    nickname: str
    avatar_text: str
    avatar_url: str | None = None
    platform: Literal["wechat", "ios", "android", "h5"]
    is_vip: bool
    vip_level: Literal["none", "monthly", "season", "yearly"]
    vip_expires_at: str | None = None
    drift_coins: int
    gender: Literal["female", "male", "unknown"] = "unknown"
    age_range: str | None = None
    city: str | None = None
    face_verified: bool = False
    gender_verified: bool = False
    charm_value: int = 0


class UserProfileUpdateRequest(BaseModel):
    nickname: str | None = Field(default=None, min_length=1, max_length=40)
    avatar_text: str | None = Field(default=None, min_length=1, max_length=8)
    avatar_url: str | None = Field(default=None, max_length=500)
    gender: Literal["female", "male", "unknown"] | None = None
    city: str | None = Field(default=None, max_length=40)
    age_range: str | None = Field(default=None, max_length=24)


class QuotaItem(BaseModel):
    type: QuotaType
    label: str
    base: int
    vip_bonus: int
    ad_bonus: int
    used: int
    remaining: int


class AdRewardState(BaseModel):
    can_watch: bool
    cooldown_seconds: int
    cooldown_minutes: int
    reward_per_quota: int
    active_session_id: str | None = None
    display_type: Literal["video", "image", "link"] = "video"
    provider: str = "mock_alliance"
    placement_id: str = "reward_video_default"
    title: str = "激励视频"
    description: str = "完整观看后可获得次数奖励"
    media_url: str | None = None
    click_url: str | None = None
    countdown_seconds: int = 5
    mini_program_app_id: str | None = None
    mini_program_path: str | None = None


class CheckinState(BaseModel):
    checked_today: bool
    streak_days: int
    week_rewards: list[int]
    current_week_index: int
    last_reward: int | None = None


class MeStatus(BaseModel):
    user: UserProfile
    quotas: dict[QuotaType, QuotaItem]
    ad_reward: AdRewardState
    checkin: CheckinState


class UserRecordSummaryItem(BaseModel):
    type: Literal["bottle", "treehole", "truth", "dare", "game", "report"]
    title: str
    desc: str
    count: int


class UserActivityRecordCreateRequest(BaseModel):
    record_type: Literal["truth", "dare", "game"]
    title: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1, max_length=1000)
    visibility: str | None = Field(default=None, max_length=40)
    source_type: str | None = Field(default=None, max_length=40)
    source_id: str | None = Field(default=None, max_length=80)


class UserActivityRecordOut(BaseModel):
    id: str
    record_type: Literal["truth", "dare", "game"]
    title: str
    content: str
    visibility: str | None = None
    source_type: str | None = None
    source_id: str | None = None
    created_at: str


class ConsumeQuotaRequest(BaseModel):
    quota_type: QuotaType
    business_id: str = Field(min_length=3)


class BottleCreateRequest(BaseModel):
    content: str = Field(min_length=1, max_length=240)
    target_gender: Literal["all", "female", "male"] = "all"
    target_scope: Literal["all", "same_city", "nearby"] = "all"


class BottleReplyRequest(BaseModel):
    content: str = Field(min_length=1, max_length=200)


class BottlePromptOut(BaseModel):
    content: str


class BottleOut(BaseModel):
    id: str
    author_id: str = "200000000001"
    author_name: str
    author_avatar_text: str | None = None
    author_avatar_url: str | None = None
    author_vip: bool = False
    author_gender: Literal["female", "male", "unknown"] = "unknown"
    author_age_range: str | None = None
    author_city: str | None = None
    author_verified: bool = False
    content: str
    mood: str
    status: ContentStatus
    replies: int
    target_gender: Literal["all", "female", "male"] = "all"
    target_scope: Literal["all", "same_city", "nearby"] = "all"
    is_following: bool = False
    friend_requested: bool = False
    created_at: str


class TreeholeCreateRequest(BaseModel):
    content: str = Field(min_length=1, max_length=280)


class TreeholePostOut(BaseModel):
    id: str
    author_id: str = "200000000001"
    author_name: str = "匿名树洞"
    author_avatar_text: str = "匿"
    author_avatar_url: str | None = None
    author_gender: Literal["female", "male", "unknown"] = "unknown"
    author_age_range: str | None = None
    content: str
    resonance_count: int
    reply_count: int
    paid_photo_count: int = 0
    status: ContentStatus
    created_at: str


class TruthQuestionOut(BaseModel):
    id: str
    category: str
    text: str


class DareTaskOut(BaseModel):
    id: str
    category: str
    text: str


class GamePromptOut(BaseModel):
    id: str
    mode: Literal["truth_public", "truth_private", "dare_public", "dare_private"]
    text: str
    meaning: str
    visibility: str


class GameRandomMatchRequest(BaseModel):
    mode: Literal["truth", "dare"] = "truth"
    gender: Literal["all", "female", "male"] = "all"
    age_range: str | None = Field(default=None, max_length=24)
    client_match_id: str = Field(min_length=3, max_length=120)


class GameRandomMatchResponse(BaseModel):
    match_id: str
    room_id: str
    mode: Literal["truth", "dare"]
    status: Literal["matched"]
    target_user: "NearbyUser"
    quota: QuotaItem
    source_type: Literal["game_room"]
    source_id: str
    evidence_id: str
    next_action: Literal["wait_confirm"]


class AdPrepareResponse(BaseModel):
    reward_session_id: str
    reward_per_quota: int
    countdown_seconds: int = 5
    provider: str = "mock_alliance"
    placement_id: str = "reward_video_default"


class AdCommitRequest(BaseModel):
    reward_session_id: str
    completed: bool


class ReportRequest(BaseModel):
    target_type: Literal["user", "bottle", "treehole", "reply", "chat", "plaza", "private_photo"]
    target_id: str
    reason: str = Field(min_length=1, max_length=160)


class BlockRequest(BaseModel):
    blocked_user_id: str


class RelationRequest(BaseModel):
    target_user_id: str


class FriendRequestOut(BaseModel):
    id: str
    requester_id: str
    target_user_id: str
    status: Literal["requested", "accepted", "rejected", "cancelled"]
    created_at: str


class FriendshipOut(BaseModel):
    id: str
    user_id: str
    friend_user_id: str
    status: Literal["active", "removed"]
    created_at: str


class RelationStateOut(BaseModel):
    target_user_id: str
    state: Literal["stranger", "pending_incoming", "pending_outgoing", "friend", "blocked"]
    can_chat: bool
    can_request_friend: bool


class WalletState(BaseModel):
    recharge_coins: int
    earned_coins: int
    gift_coins: int
    withdrawable_coins: int
    frozen_coins: int
    charm_value: int
    withdraw_threshold_charm: int
    charm_exchange_rate: int


class CoinLedgerItem(BaseModel):
    id: str
    title: str
    amount: int
    coin_bucket: Literal["recharge", "earned", "gift"]
    withdrawable: bool
    created_at: str


class CreatorProfile(BaseModel):
    user_id: str
    display_name: str
    gender: Literal["female", "male", "unknown"]
    verified: bool
    safety_score: int
    follower_count: int
    album_count: int
    earned_coins: int
    charm_value: int


class PrivatePhoto(BaseModel):
    id: str
    owner_id: str
    owner_name: str
    title: str
    cover_tone: str = "mint"
    price_coins: int
    blurred: bool = True
    status: ContentStatus
    purchased: bool


class GiftProduct(BaseModel):
    id: str
    name: str
    price_coins: int
    icon_text: str


class UnlockPhotoRequest(BaseModel):
    photo_id: str


class SendGiftRequest(BaseModel):
    gift_id: str
    receiver_id: str


class ConversationGiftRequest(BaseModel):
    gift_id: str


class WithdrawRequest(BaseModel):
    amount: int = Field(gt=0)


class VerificationState(BaseModel):
    face_verified: bool
    gender_verified: bool
    detected_gender: Literal["female", "male", "unknown"]
    liveness_passed: bool
    manual_review_status: Literal["not_submitted", "pending", "approved", "rejected"]


class VerificationReviewRequest(BaseModel):
    action: Literal["approve", "reject"]
    reason: str | None = Field(default=None, max_length=160)


class ReferralState(BaseModel):
    invite_code: str
    invited_count: int
    reward_vip_days: int
    next_reward_need: int


class BlacklistItem(BaseModel):
    id: str
    user_id: str
    nickname: str
    reason: str
    blocked_at: str


class PlazaMediaCreate(BaseModel):
    media_type: Literal["image", "voice", "video"]
    url: str = Field(min_length=1, max_length=500)
    mime_type: str = Field(min_length=1, max_length=120)
    storage_key: str | None = Field(default=None, max_length=240)
    size_bytes: int | None = Field(default=None, ge=0)
    duration_seconds: int | None = Field(default=None, ge=0)
    width: int | None = Field(default=None, ge=0)
    height: int | None = Field(default=None, ge=0)


class PlazaMediaOut(PlazaMediaCreate):
    id: str
    post_id: str
    owner_id: str
    created_at: str


class PlazaPost(BaseModel):
    id: str
    author_id: str
    author_name: str
    icon_text: str
    icon_url: str | None = None
    topic: str
    content: str
    media_type: Literal["text", "image", "voice", "video"] = "text"
    media_count: int = 0
    gender: Literal["female", "male", "unknown"] = "unknown"
    verified: bool = False
    city: str | None = None
    age_range: str | None = None
    view_count: int = 0
    like_count: int
    liked_by_current_user: bool = False
    comment_count: int
    comment_preview: str | None = None
    media: list[PlazaMediaOut] = Field(default_factory=list)
    distance_text: str | None = None
    created_at: str


class PlazaCreateRequest(BaseModel):
    content: str = Field(min_length=1, max_length=180)
    media_type: Literal["text", "image", "voice", "video"] = "text"
    media_count: int = 0
    media: list[PlazaMediaCreate] = Field(default_factory=list, max_length=9)


class PlazaCommentRequest(BaseModel):
    content: str = Field(min_length=1, max_length=120)
    hidden_for_owner_only: bool = False


class PlazaCommentOut(BaseModel):
    id: str
    post_id: str
    author_id: str
    author_name: str
    icon_text: str
    icon_url: str | None = None
    author_gender: Literal["female", "male", "unknown"] = "unknown"
    author_age_range: str | None = None
    author_verified: bool = False
    author_city: str | None = None
    content: str
    hidden_for_owner_only: bool = False
    visible_to_owner_only: bool = False
    created_at: str


class NearbyUser(BaseModel):
    id: str
    nickname: str
    icon_text: str
    icon_url: str | None = None
    gender: Literal["female", "male", "unknown"]
    verified: bool
    age_range: str | None = None
    city: str | None = None
    distance_km: float | None = None
    distance_text: str
    signature: str
    is_vip: bool
    online: bool


class MembershipProduct(BaseModel):
    id: str
    name: str
    price_label: str
    platform: Literal["wechat", "ios", "android", "all"]
    benefits: list[str]


class OrderVerifyRequest(BaseModel):
    platform: Literal["wechat", "ios", "android"]
    product_id: str
    transaction_id: str
    receipt: str


class AdminRewardConfig(BaseModel):
    base_quotas: dict[QuotaType, int]
    vip_bonus: dict[QuotaType, int]
    ad_cooldown_minutes: int
    ad_reward_per_quota: int = Field(default=1, ge=1, le=50)
    checkin_rewards: list[int]
    reject_refund_enabled: bool = False
    ad_display_type: Literal["video", "image", "link"] = "video"
    ad_provider: str = Field(default="mock_alliance", max_length=80)
    ad_placement_id: str = Field(default="reward_video_default", max_length=120)
    ad_title: str = Field(default="激励视频", max_length=80)
    ad_description: str = Field(default="完整观看后可获得次数奖励", max_length=200)
    ad_media_url: str | None = Field(default=None, max_length=500)
    ad_click_url: str | None = Field(default=None, max_length=500)
    ad_countdown_seconds: int = Field(default=5, ge=3, le=60)
    mini_program_app_id: str | None = Field(default=None, max_length=80)
    mini_program_path: str | None = Field(default=None, max_length=200)


class AdminSummary(BaseModel):
    users: int
    pending_content: int
    reports: int
    ad_rewards_today: int
    orders_today: int


class ActionResponse(BaseModel):
    status: str
    target_id: str | None = None
    message: str | None = None


class ReportOut(BaseModel):
    id: str
    reporter_id: str | None = None
    target_type: Literal["user", "bottle", "treehole", "reply", "chat", "plaza", "private_photo"]
    target_id: str
    reason: str
    status: Literal["queued", "reviewing", "resolved"]
    created_at: str
    target_type_text: str | None = None
    target_display_name: str | None = None
    target_avatar_text: str | None = None
    target_avatar_url: str | None = None
    target_preview: str | None = None
    evidence_refs: list[str] = Field(default_factory=list)
    audit_refs: list[str] = Field(default_factory=list)


class AdminReportResolveRequest(BaseModel):
    action: Literal["resolve"] = "resolve"
    reason: str = Field(min_length=1, max_length=200)
    penalty_action: Literal["none", "limit_user", "freeze_chat", "offline_content"] = "none"


class AdminReportResolveResponse(BaseModel):
    report_id: str
    before_status: Literal["queued", "reviewing", "resolved"]
    after_status: Literal["queued", "reviewing", "resolved"]
    reason: str
    audit_id: str
    resolved_at: str
    penalty_action: Literal["none", "limit_user", "freeze_chat", "offline_content"] = "none"
    penalty_target_user_id: str | None = None
    penalty_target_thread_id: str | None = None
    penalty_target_content_id: str | None = None
    penalty_target_content_type: str | None = None
    penalty_audit_id: str | None = None


class AdminReportRestoreRequest(BaseModel):
    reason: str = Field(min_length=1, max_length=200)


class AdminReportRestoreResponse(BaseModel):
    report_id: str
    thread_id: str
    before_thread_status: Literal["active", "risk_frozen"]
    after_thread_status: Literal["active", "risk_frozen"]
    reason: str
    audit_id: str
    restored_at: str


class ChatAppealCreateRequest(BaseModel):
    reason: str = Field(min_length=1, max_length=240)


class ChatAppealOut(BaseModel):
    id: str
    thread_id: str
    user_id: str
    user_name: str | None = None
    participant_name: str | None = None
    reason: str
    status: Literal["pending", "approved", "rejected"]
    admin_reason: str | None = None
    audit_refs: list[str] = Field(default_factory=list)
    created_at: str
    updated_at: str


class AdminChatAppealReviewRequest(BaseModel):
    action: Literal["approve", "reject"]
    reason: str = Field(min_length=1, max_length=240)


class AdminChatAppealReviewResponse(BaseModel):
    appeal_id: str
    thread_id: str
    before_status: Literal["pending", "approved", "rejected"]
    after_status: Literal["pending", "approved", "rejected"]
    thread_status: Literal["active", "risk_frozen"]
    audit_id: str
    reviewed_at: str


class BlockOut(BaseModel):
    id: str
    blocked_user_id: str
    status: Literal["blocked", "unblocked"]
    blocked_at: str


class MembershipOrderOut(BaseModel):
    id: str
    platform: Literal["wechat", "ios", "android"]
    product_id: str
    transaction_id: str
    status: Literal["mock_verified", "duplicate_verified"]
    vip_level: Literal["monthly", "season", "yearly"]
    verified_at: str


class OrderVerifyResponse(BaseModel):
    order: MembershipOrderOut
    user: UserProfile


class AdminUserOut(BaseModel):
    id: str
    nickname: str
    avatar_text: str | None = None
    avatar_url: str | None = None
    platform: Literal["wechat", "ios", "android", "h5"]
    gender: Literal["female", "male", "unknown"]
    is_vip: bool
    drift_coins: int
    status: Literal["active", "limited", "blocked"]
    face_verified: bool
    created_at: str
    blocked_until: str | None = None
    block_reason: str | None = None


class AdminUserStatusRequest(BaseModel):
    status: Literal["active", "limited", "blocked"]
    reason: str | None = None
    block_days: int | None = Field(default=None, ge=0, le=365)
    blocked_until: str | None = None


class AdminContentOut(BaseModel):
    id: str
    type: Literal["bottle", "treehole", "plaza", "private_photo"]
    status: ContentStatus
    author_id: str
    author_name: str | None = None
    author_avatar_text: str | None = None
    author_avatar_url: str | None = None
    excerpt: str
    created_at: str


class ModerationDecisionRequest(BaseModel):
    action: Literal["approve", "reject", "dismiss", "ban"]
    reason: str | None = None


class AdminModerationJobOut(BaseModel):
    job_id: str
    status: Literal["processed"]
    action: Literal["approve", "reject", "dismiss", "ban"]
    reason: str | None
    audited_at: str


class AdminAuditLogOut(BaseModel):
    id: str
    actor: str
    action: str
    target_type: str
    target_id: str
    detail: str | None = None
    created_at: str


class AdminWalletSummary(BaseModel):
    recharge_coins: int
    earned_coins: int
    gift_coins: int
    frozen_coins: int
    pending_withdrawals: int


class AdminLoginRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)


class AdminPrincipalOut(BaseModel):
    username: str
    roles: list[str]


class AdminTokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"]
    expires_in: int
    admin: AdminPrincipalOut


class AdminLogoutResponse(BaseModel):
    status: Literal["logged_out"]


class WalletOverview(BaseModel):
    wallet: WalletState
    ledger: list[CoinLedgerItem]
    gifts: list[GiftProduct]


class VerificationOverview(BaseModel):
    verification: VerificationState
    referral: ReferralState


class ReferralClaimResponse(BaseModel):
    status: Literal["claimed", "not_enough"]
    referral: ReferralState


class PhotoUnlockResponse(BaseModel):
    photo: PrivatePhoto
    wallet: WalletState


class GiftSendResponse(BaseModel):
    status: Literal["sent"]
    receiver_id: str
    wallet: WalletState


class WithdrawResponse(BaseModel):
    status: Literal["reviewing"]
    wallet: WalletState


class TreeholeReactResponse(BaseModel):
    status: Literal["ok"]
    post: TreeholePostOut


class MessageItemOut(BaseModel):
    id: str
    title: str
    body: str
    created_at: str
    unread: bool
    business_type: str | None = None
    business_id: str | None = None


class ConversationTurnOut(BaseModel):
    id: str
    sender_name: str
    body: str
    created_at: str
    from_me: bool
    type: Literal["text", "image", "voice", "video", "flash_image", "flash_video", "gift", "game_room"] = "text"
    media_url: str | None = None
    media_duration: int | None = None
    flash_viewed: bool = False
    gift_id: str | None = None
    gift_name: str | None = None
    gift_icon_text: str | None = None
    gift_price_coins: int | None = None
    game_room_id: str | None = None
    game_room_mode: Literal["truth", "dare", "mixed"] | None = None


class AdminChatReviewOut(BaseModel):
    id: str
    thread_id: str
    source: Literal["bottle", "treehole", "plaza", "game_room"]
    participant_user_ids: list[str]
    participants: list[str]
    related_content: str
    last_message: str
    risk_level: Literal["low", "medium", "high"]
    status: Literal["pending", "reviewing", "resolved"]
    review_trigger: Literal["report", "keyword", "risk"]
    handling_policy: str
    matched_keywords: list[str] = []
    auto_action: Literal["mask_and_review", "reject", "manual_review"]
    reason: str
    messages: list[ConversationTurnOut]
    discipline_status: Literal["clear", "watch", "violation"] = "clear"
    discipline_summary: str = ""
    room_mode: Literal["truth", "dare", "mixed"] | None = None
    participant_avatar_texts: list[str | None] = []
    participant_avatar_urls: list[str | None] = []
    updated_at: str


class ConversationThreadOut(BaseModel):
    id: str
    bottle_id: str | None = None
    status: Literal["active", "risk_frozen"] = "active"
    frozen_notice: str | None = None
    participant_user_id: str
    participant_name: str
    participant_avatar_text: str | None = None
    participant_avatar_url: str | None = None
    participant_tag: str
    bottle_preview: str | None = None
    last_message: str | None = None
    updated_at: str
    unread_count: int
    turns: list[ConversationTurnOut]


class ConversationTurnCreate(BaseModel):
    body: str = Field(min_length=1, max_length=500)
    type: Literal["text", "image", "voice", "video", "flash_image", "flash_video"] = "text"
    media_url: str | None = Field(default=None, max_length=500)
    media_duration: int | None = Field(default=None, ge=0)


class GameRoomCreate(BaseModel):
    mode: Literal["truth", "dare", "mixed"]


class GameRoomCreateResponse(BaseModel):
    room_id: str
    thread: ConversationThreadOut


class ConversationGiftResponse(BaseModel):
    wallet: WalletState
    thread: ConversationThreadOut


class WalletRechargeRequest(BaseModel):
    amount: int = Field(gt=0)
    channel: Literal["wechat", "apple", "android", "mock"] = "mock"


class WalletRechargeResponse(BaseModel):
    order_id: str
    wallet: WalletState


PrivatePhotoReviewStatus = Literal["ai_pending", "ai_approved", "manual_required", "manual_approved", "rejected", "frozen", "appeal_pending"]
PrivatePhotoRiskLevel = Literal["low_risk", "medium_risk", "high_risk"]
PrivatePhotoRevenueState = Literal["frozen", "eligible", "ineligible"]


class PrivatePhotoCreateRequest(BaseModel):
    file_id: str | None = Field(default=None, max_length=120)
    upload_token: str | None = Field(default=None, max_length=120)
    visibility: Literal["private"] = "private"
    caption: str | None = Field(default=None, max_length=160)
    client_upload_id: str | None = Field(default=None, max_length=120)


class PrivatePhotoReviewOut(BaseModel):
    id: str
    owner_id: str
    review_status: PrivatePhotoReviewStatus
    risk_level: PrivatePhotoRiskLevel
    model_labels: list[str]
    confidence: float
    auto_action: Literal["approve", "manual_review", "reject", "freeze"]
    revenue_state: PrivatePhotoRevenueState
    user_visible_message: str
    created_at: str
    manual_review: dict[str, str] | None = None
    appeal_state: str | None = None
    audit_refs: list[str] = Field(default_factory=list)


class PrivatePhotoUnlockNewResponse(BaseModel):
    unlock_id: str
    photo_id: str
    charged_amount: int
    creator_revenue_state: PrivatePhotoRevenueState
    audit_id: str


class PrivatePhotoAppealRequest(BaseModel):
    reason: str = Field(min_length=1, max_length=200)


class PrivatePhotoAppealResponse(BaseModel):
    photo_id: str
    review_status: PrivatePhotoReviewStatus
    appeal_state: str
    revenue_state: PrivatePhotoRevenueState
    audit_id: str


class AdminPrivatePhotoReviewOut(BaseModel):
    id: str
    photo_id: str
    user_id: str
    review_status: PrivatePhotoReviewStatus
    risk_level: PrivatePhotoRiskLevel
    model_labels: list[str]
    confidence: float
    auto_action: Literal["approve", "manual_review", "reject", "freeze"]
    report_count: int = 0
    revenue_state: PrivatePhotoRevenueState
    assigned_admin_id: str | None = None
    updated_at: str


class AdminPrivatePhotoReviewRequest(BaseModel):
    action: Literal["approve", "reject", "freeze", "unfreeze", "request_more_review"]
    reason: str = Field(min_length=1, max_length=200)
    manual_labels: list[str] = Field(default_factory=list)
    revenue_action: Literal["keep_frozen", "release", "forfeit"] = "keep_frozen"


class AdminPrivatePhotoReviewResponse(BaseModel):
    review_id: str
    before_status: PrivatePhotoReviewStatus
    after_status: PrivatePhotoReviewStatus
    before_revenue_state: PrivatePhotoRevenueState
    after_revenue_state: PrivatePhotoRevenueState
    audit_id: str


class AdminPrivatePhotoRiskSummary(BaseModel):
    low_risk: int
    medium_risk: int
    high_risk: int
    manual_required: int
    frozen: int


ChatSourceType = Literal["bottle_reply", "plaza_comment", "treehole_comment", "game_room", "private_room", "match_expand", "friend"]
ChatConversationStatus = Literal["pending", "active", "muted", "blocked", "expired", "reported", "risk_frozen"]


class ChatContextRequestCreate(BaseModel):
    target_user_id: str = Field(min_length=1, max_length=80)
    source_type: ChatSourceType
    source_id: str | None = Field(default=None, max_length=120)
    reply_id: str | None = Field(default=None, max_length=120)
    initiator_action: Literal["reply", "continue_chat", "private_chat", "room_confirm"]
    evidence_id: str | None = Field(default=None, max_length=120)


class ChatContextRequestAccept(BaseModel):
    confirm_action: Literal["reply", "continue_chat", "private_chat", "room_confirm"]
    evidence_id: str = Field(min_length=1, max_length=120)


class ChatContextRequestReject(BaseModel):
    reason: str = Field(min_length=1, max_length=160)


class ChatContextRequestOut(BaseModel):
    id: str
    status: ChatConversationStatus
    conversation_id: str | None = None
    source_type: ChatSourceType
    source_id: str | None = None
    source_summary: dict[str, str]
    rate_limit: dict[str, int | str]


class MatchExpandContextResponse(BaseModel):
    request: ChatContextRequestOut
    gate: Literal["vip", "drift_coins"]
    cost_coins: int
    remaining_drift_coins: int
    user: UserProfile
    thread_id: str | None = None


class ChatMessageCreate(BaseModel):
    content_type: Literal["text", "image", "voice", "video", "system_source_card"] = "text"
    content: str = Field(min_length=1, max_length=500)
    client_message_id: str | None = Field(default=None, max_length=120)


class ChatMessageOut(BaseModel):
    id: str
    sender_id: str
    client_message_id: str | None = None
    sequence: int
    content_type: Literal["text", "image", "voice", "video", "system_source_card"]
    content: str
    status: Literal["sent", "risk_pending", "blocked"]
    created_at: str


class ChatConversationOut(BaseModel):
    id: str
    status: ChatConversationStatus
    source_type: ChatSourceType
    source_id: str | None = None
    source_summary: dict[str, str]
    participants: list[str]
    friendship_state: Literal["none", "friend"] = "none"
    expires_at: str | None = None
    last_message: str | None = None
    rate_limit: dict[str, int | str] = Field(default_factory=dict)
    risk_state: Literal["clear", "reported", "risk_frozen", "blocked"] = "clear"
    report_state: Literal["none", "reported"] = "none"
    messages: list[ChatMessageOut] = Field(default_factory=list)
    audit_refs: list[str] = Field(default_factory=list)


class ChatMessageSendResponse(BaseModel):
    message_id: str
    sequence: int
    deduplicated: bool = False
    status: Literal["sent", "risk_pending", "blocked"]
    risk_labels: list[str] = Field(default_factory=list)
    audit_id: str


class ChatMessageSyncResponse(BaseModel):
    conversation_id: str
    after_sequence: int
    latest_sequence: int
    has_more: bool
    messages: list[ChatMessageOut] = Field(default_factory=list)


class ChatReadCursorUpdate(BaseModel):
    last_read_sequence: int = Field(ge=0)


class ChatReadCursorOut(BaseModel):
    conversation_id: str
    user_id: str
    last_read_sequence: int
    updated_at: str


class RoomCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    visibility: Literal["private", "public"]
    size_mode: Literal["pair", "group"] = "pair"
    join_policy: Literal["invite", "approval", "open"] = "invite"
    capacity: int = Field(default=2, ge=2, le=20)
    allow_member_invite: bool = False
    conversation_id: str | None = Field(default=None, max_length=64)


class UploadPrepareRequest(BaseModel):
    filename: str = Field(min_length=1, max_length=160)
    content_type: Literal["image/jpeg", "image/png", "image/webp", "video/mp4", "audio/mpeg", "audio/mp4"]
    size_bytes: int = Field(gt=0, le=20 * 1024 * 1024)


class UploadPrepareResponse(BaseModel):
    object_key: str
    upload_url: str
    public_url: str
    expires_in_seconds: int


class RoomMemberOut(BaseModel):
    user_id: str
    role: Literal["owner", "moderator", "member"]
    status: Literal["invited", "active", "left", "removed"]


class RoomOut(BaseModel):
    id: str
    owner_id: str
    conversation_id: str | None = None
    name: str
    visibility: Literal["private", "public"]
    size_mode: Literal["pair", "group"]
    join_policy: Literal["invite", "approval", "open"]
    capacity: int
    allow_member_invite: bool
    status: Literal["active", "ended", "closed"]
    members: list[RoomMemberOut] = Field(default_factory=list)
    created_at: str


class RoomInvitationCreate(BaseModel):
    invitee_id: str = Field(min_length=1, max_length=64)
    idempotency_key: str = Field(min_length=3, max_length=120)


class RoomInvitationOut(BaseModel):
    id: str
    room_id: str
    inviter_id: str
    invitee_id: str
    status: Literal["pending", "accepted", "rejected", "expired"]
    expires_at: str


class GameRoundCreate(BaseModel):
    mode: Literal["truth", "dare", "dice"]


class GameRoundOut(BaseModel):
    id: str
    room_id: str
    initiator_id: str
    mode: Literal["truth", "dare", "dice"]
    status: Literal["waiting", "active", "resolved", "expired", "cancelled"]
    prompt_id: str | None = None
    prompt_text: str | None = None
    result: dict = Field(default_factory=dict)
    created_at: str
    resolved_at: str | None = None


class ChatConversationReportRequest(BaseModel):
    reason: str = Field(min_length=1, max_length=160)
    message_ids: list[str] = Field(default_factory=list)
    description: str | None = Field(default=None, max_length=500)


class ChatConversationReportResponse(BaseModel):
    report_id: str
    conversation_status: ChatConversationStatus
    audit_id: str


class ChatConversationBlockRequest(BaseModel):
    target_user_id: str = Field(min_length=1, max_length=80)
    reason: str = Field(min_length=1, max_length=160)


class ChatConversationBlockResponse(BaseModel):
    block_id: str
    conversation_status: ChatConversationStatus
    audit_id: str
