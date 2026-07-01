from __future__ import annotations

import asyncio
import hashlib
import json
from contextvars import ContextVar
from datetime import UTC, date, datetime, timedelta
from random import choice
from urllib.parse import quote
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import and_, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import (
    AdRewardSession,
    AdminAuditLog,
    AdminUserRestriction,
    AppConfig,
    BlacklistEntry,
    Bottle,
    BottleReply,
    ChatAppeal,
    ChatContextRequestRecord,
    CheckinRecord,
    CoinLedger,
    ContentReport,
    ConversationThread,
    ConversationTurn,
    Follow,
    FriendRequest,
    GameRoom,
    GiftOrder,
    GiftProduct,
    MembershipOrder,
    MembershipProductConfig,
    MessageNotification,
    PaymentOrder,
    PlazaComment,
    PlazaLike,
    PlazaMedia,
    PlazaPost,
    PrivatePhotoAsset,
    PromptTemplate,
    QuotaBalance,
    ReferralAccount,
    TreeholePost,
    TreeholeReaction,
    TreeholeReply,
    UserActivityRecord,
    User,
    VerificationProfile,
    WalletAccount,
)
from app.schemas import (
    AdminRewardConfig,
    AdRewardState,
    BlacklistItem,
    BlockOut,
    BottleOut,
    ChatContextRequestCreate,
    ChatAppealOut,
    CheckinState,
    CoinLedgerItem,
    AdminChatReviewOut,
    ConversationThreadOut,
    ConversationTurnOut,
    CreatorProfile,
    GiftProduct as GiftProductOut,
    GameRandomMatchRequest,
    GameRandomMatchResponse,
    GamePromptOut,
    MeStatus,
    MatchExpandContextResponse,
    MembershipProduct,
    MessageItemOut,
    MembershipOrderOut,
    NearbyUser,
    PhotoUnlockResponse,
    PlazaCommentOut,
    PlazaMediaOut,
    PlazaPost as PlazaPostOut,
    PrivatePhoto,
    QuotaItem,
    QuotaType,
    ReferralState,
    ReportOut,
    DareTaskOut,
    TreeholePostOut,
    TruthQuestionOut,
    UserActivityRecordCreateRequest,
    UserActivityRecordOut,
    UserProfile,
    UserProfileUpdateRequest,
    UserRecordSummaryItem,
    VerificationState,
    WalletState,
)

DEFAULT_USER_ID = "100000000001"
CREATOR_IDS = {
    "creator_001": "200000000001",
    "creator_002": "200000000002",
    "creator_003": "200000000003",
    "creator_004": "200000000004",
    "creator_005": "200000000005",
    "creator_006": "200000000006",
    "creator_007": "200000000007",
    "creator_008": "200000000008",
    "bad_user_001": "299000000001",
}
CURRENT_USER_ID: ContextVar[str] = ContextVar("current_user_id", default=DEFAULT_USER_ID)
SEED_LOCK = asyncio.Lock()
CHECKIN_REWARDS = [10, 10, 30, 10, 10, 30, 100]
BASE_QUOTAS: dict[QuotaType, tuple[str, int]] = {
    QuotaType.fish_bottle: ("捞瓶", 10),
    QuotaType.throw_bottle: ("扔瓶", 5),
    QuotaType.truth: ("真心话", 5),
    QuotaType.dare: ("大冒险", 5),
    QuotaType.treehole_post: ("树洞", 4),
}
SYSTEM_AVATAR_SEEDS = [f"bottle-wave-{index:02d}" for index in range(1, 31)]
MATCH_EXPAND_CHAT_COST = 5
AD_REWARD_CONFIG_KEY = "ad_reward_config"
DEFAULT_AD_MEDIA_URL = "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
CHAT_RISK_WORDS = ["wechat", "wx", "qq", "telegram", "phone", "mobile", "bank", "transfer", "cash", "微信", "QQ", "手机号", "站外", "私下", "转账"]
GAME_DISCIPLINE_WORDS = ["刷屏", "辱骂", "威胁", "约线下", "越界", "站外", "私下", "转账", "微信", "QQ", "手机号", "telegram", "wx"]
TRUTH_QUESTIONS = [
    ("truth_001", "关系", "最近一次让你心动的小细节是什么？"),
    ("truth_002", "自我", "你最希望别人理解你的哪一面？"),
    ("truth_003", "秘密", "你有没有一个一直没说出口的遗憾？"),
]


def default_ad_reward_config() -> dict:
    return {
        "base_quotas": {quota_type.value: base for quota_type, (_, base) in BASE_QUOTAS.items()},
        "vip_bonus": {quota_type.value: 5 for quota_type in BASE_QUOTAS},
        "ad_cooldown_minutes": 15,
        "ad_reward_per_quota": 10,
        "checkin_rewards": CHECKIN_REWARDS,
        "reject_refund_enabled": False,
        "ad_display_type": "video",
        "ad_provider": "mock_alliance",
        "ad_placement_id": "reward_video_default",
        "ad_title": "漂流岛激励视频",
        "ad_description": "完整观看倒计时后，所有玩法次数都会增加。",
        "ad_media_url": DEFAULT_AD_MEDIA_URL,
        "ad_click_url": "https://example.com/drift-ad",
        "ad_countdown_seconds": 5,
        "mini_program_app_id": "wx-drift-bottle-demo",
        "mini_program_path": "pages/ad/reward",
    }


async def get_admin_reward_config(session: AsyncSession) -> AdminRewardConfig:
    data = default_ad_reward_config()
    row = await session.get(AppConfig, AD_REWARD_CONFIG_KEY)
    if row is not None:
        try:
            stored = json.loads(row.value)
        except json.JSONDecodeError:
            stored = {}
        if isinstance(stored, dict):
            data.update(stored)
    return AdminRewardConfig(**data)


async def update_admin_reward_config(
    session: AsyncSession,
    payload: AdminRewardConfig,
    actor: str,
) -> AdminRewardConfig:
    data = default_ad_reward_config()
    data.update(payload.model_dump())
    row = await session.get(AppConfig, AD_REWARD_CONFIG_KEY)
    if row is None:
        row = AppConfig(key=AD_REWARD_CONFIG_KEY, value="", updated_by=actor, updated_at=now())
        session.add(row)
    row.value = json.dumps(data, ensure_ascii=False)
    row.updated_by = actor
    row.updated_at = now()
    session.add(
        AdminAuditLog(
            id=new_id("audit"),
            actor=actor,
            action="update_ad_reward_config",
            target_type="reward_config",
            target_id="ad_reward",
            detail=f"provider={data['ad_provider']};placement={data['ad_placement_id']}",
            created_at=now(),
        )
    )
    await session.commit()
    return AdminRewardConfig(**data)
DARE_TASKS = [
    ("dare_001", "轻松", "给最近聊天的人发一句真诚夸奖。"),
    ("dare_002", "互动", "用 30 秒语音描述此刻窗外的声音。"),
    ("dare_003", "勇气", "邀请对方开一个真心话房间。"),
]
GAME_PROMPTS = [
    ("game_truth_public_001", "truth_public", "你最近一次真正心动，是因为哪个细节？", "从轻松细节切入，适合破冰和朋友局。", "所有参与者可见"),
    ("game_truth_public_002", "truth_public", "如果今晚可以收到一句话，你最想听见什么？", "让回答保留想象空间，不强迫暴露隐私。", "所有参与者可见"),
    ("game_truth_public_003", "truth_public", "有没有一个瞬间，让你突然觉得自己被理解了？", "温和地聊连接感，适合公开场景。", "所有参与者可见"),
    ("game_truth_private_001", "truth_private", "如果我靠近一点，你会先躲开，还是先看着我？", "暧昧地试探边界和心动反应，只适合双方同意的私密局。", "仅双方可见"),
    ("game_truth_private_002", "truth_private", "你最容易被哪种眼神、语气或小动作撩到？", "用诱惑但不冒犯的方式聊吸引力偏好。", "仅双方可见"),
    ("game_truth_private_003", "truth_private", "如果今晚只能说一句带暗示的话，你会怎么说？", "把暧昧交给表达，不要求现实行动。", "仅双方可见"),
    ("game_dare_public_001", "dare_public", "用 20 个字夸一下今天的自己。", "轻量表达任务，适合公开完成。", "所有参与者可见"),
    ("game_dare_public_002", "dare_public", "给一个很久没联系的人发一句不打扰的问候。", "温和行动挑战，不涉及隐私暴露。", "所有参与者可见"),
    ("game_dare_public_003", "dare_public", "拍一张只代表此刻心情的照片，不需要露脸。", "用画面表达状态，公开场景也安全。", "所有参与者可见"),
    ("game_dare_private_001", "dare_private", "发一句让对方忍不住多看两遍的晚安。", "带一点诱惑感的文字挑战，重点是氛围，不越界。", "仅双方可见"),
    ("game_dare_private_002", "dare_private", "用一句话描述你想被怎样靠近。", "私密地表达期待，同时保留边界。", "仅双方可见"),
    ("game_dare_private_003", "dare_private", "给对方留一个只适合今晚看的暗号。", "制造亲密感和专属感，只适合双方可见。", "仅双方可见"),
]


def now() -> datetime:
    return datetime.now(UTC)


def iso(value: datetime | None) -> str:
    return (value or now()).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex}"


def system_avatar_url(seed: str) -> str:
    digest = hashlib.sha1((seed or "anonymous").encode("utf-8")).hexdigest()
    avatar_seed = SYSTEM_AVATAR_SEEDS[int(digest[:8], 16) % len(SYSTEM_AVATAR_SEEDS)]
    return f"https://api.dicebear.com/9.x/open-peeps/svg?seed={quote(avatar_seed)}&backgroundColor=b6e3f4,c0aede,d1d4f9"


def resolved_avatar_url(user: User | None, seed: str) -> str:
    return user.avatar_url if user and user.avatar_url else system_avatar_url(seed)


def stable_user_seed_id(prefix: str, key: str, user_id: str | None = None) -> str:
    owner_id = user_id or current_user_id()
    digest = hashlib.sha1(f"{owner_id}:{key}".encode("utf-8")).hexdigest()[:16]
    return f"{prefix}_{digest}"


def invite_code_for_user(user_id: str) -> str:
    if user_id == DEFAULT_USER_ID:
        return "SEA260"
    digest = hashlib.sha1(user_id.encode("utf-8")).hexdigest()[:10].upper()
    return f"SEA{digest}"


def normalize_user_id(user_id: str | None) -> str:
    normalized = (user_id or "").strip()
    if not normalized:
        return DEFAULT_USER_ID
    if normalized.isdigit():
        return normalized[:64]
    digest = int(hashlib.sha1(normalized.encode("utf-8")).hexdigest()[:14], 16)
    return f"9{digest % 10_000_000_000_000:013d}"


def set_current_user_id(user_id: str | None):
    return CURRENT_USER_ID.set(normalize_user_id(user_id))


def reset_current_user_id(token) -> None:
    CURRENT_USER_ID.reset(token)


def current_user_id() -> str:
    return CURRENT_USER_ID.get()


async def ensure_seed_data(session: AsyncSession) -> User:
    async with SEED_LOCK:
        return await _ensure_seed_data_unlocked(session)


async def _ensure_seed_data_unlocked(session: AsyncSession) -> User:
    user = await session.get(User, current_user_id())
    if user is None:
        user = User(
            id=current_user_id(),
            nickname="海风来信",
            role="user",
            avatar_text="海",
            avatar_url=system_avatar_url(current_user_id()),
            platform="h5",
            gender="female",
            city="杭州",
            age_range="25-30",
            is_vip=True,
            vip_level="monthly",
            drift_coins=260,
            face_verified=True,
            gender_verified=True,
            charm_value=1880,
            status="active",
            created_at=now(),
        )
        session.add(user)
        await session.flush()
    elif not user.avatar_url:
        user.avatar_url = system_avatar_url(user.id)

    creators = [
        (CREATOR_IDS["creator_001"], "海岛来信", "证", "female", "上海", "25-30", True, True, "只接受礼貌的关注和好友申请。"),
        (CREATOR_IDS["creator_002"], "晚风", "晚", "female", "杭州", "18-24", True, False, "喜欢慢慢聊天。"),
        (CREATOR_IDS["creator_003"], "北岸", "近", "male", "杭州", "25-30", True, False, "喜欢听故事，也认真回瓶子。"),
        (CREATOR_IDS["creator_004"], "橘子海", "橘", "female", "杭州", "18-24", False, True, "傍晚适合发呆。"),
        (CREATOR_IDS["creator_005"], "小满", "满", "female", "成都", "22-26", True, False, "把今天收好，明天慢慢打开。"),
        (CREATOR_IDS["creator_006"], "蓝莓气泡", "蓝", "female", "广州", "18-24", True, False, "今天也有一点值得被记住。"),
        (CREATOR_IDS["creator_007"], "南风", "南", "male", "深圳", "25-30", False, False, "想找一个认真玩游戏的人。"),
        (CREATOR_IDS["creator_008"], "阿树", "树", "unknown", "厦门", None, False, False, "如果是晚上去，记得点靠窗的位置。"),
        (CREATOR_IDS["bad_user_001"], "无礼访客", "黑", "unknown", "未知", None, False, False, "已屏蔽用户。"),
    ]
    for user_id, nickname, avatar_text, gender, city, age_range, verified, vip, _ in creators:
        existing_creator = await session.get(User, user_id)
        if existing_creator is None:
            session.add(
                User(
                    id=user_id,
                    nickname=nickname,
                    role="creator",
                    avatar_text=avatar_text,
                    avatar_url=system_avatar_url(user_id),
                    platform="h5",
                    gender=gender,
                    city=city,
                    age_range=age_range,
                    is_vip=vip,
                    vip_level="monthly" if vip else "none",
                    drift_coins=80,
                    face_verified=verified,
                    gender_verified=verified,
                    charm_value=1200 if verified else 300,
                    status="active",
                    created_at=now(),
                )
            )
        elif not existing_creator.avatar_url:
            existing_creator.avatar_url = system_avatar_url(user_id)

    wallet = await session.get(WalletAccount, current_user_id())
    if wallet is None:
        session.add(
            WalletAccount(
                user_id=current_user_id(),
                recharge_coins=520,
                earned_coins=180,
                gift_coins=68,
                withdrawable_coins=180,
                frozen_coins=20,
                charm_value=1880,
                withdraw_threshold_charm=1000,
                charm_exchange_rate=100,
                updated_at=now(),
            )
        )

    for quota_type, (_, base) in BASE_QUOTAS.items():
        exists = await session.scalar(
            select(QuotaBalance).where(QuotaBalance.user_id == current_user_id(), QuotaBalance.quota_type == quota_type.value)
        )
        if exists is None:
            vip_bonus = 5
            session.add(
                QuotaBalance(
                    id=new_id("quota"),
                    user_id=current_user_id(),
                    quota_type=quota_type.value,
                    base=base,
                    vip_bonus=vip_bonus,
                    ad_bonus=0,
                    used=0,
                    remaining=base + vip_bonus,
                    updated_at=now(),
                )
            )

    if await session.scalar(select(VerificationProfile).where(VerificationProfile.user_id == current_user_id())) is None:
        session.add(
            VerificationProfile(
                user_id=current_user_id(),
                face_verified=True,
                gender_verified=True,
                detected_gender="female",
                liveness_passed=True,
                manual_review_status="approved",
                submitted_at=now(),
                reviewed_at=now(),
            )
        )
    if await session.scalar(select(ReferralAccount).where(ReferralAccount.user_id == current_user_id())) is None:
        invite_code = invite_code_for_user(current_user_id())
        suffix = 0
        while True:
            existing_invite = await session.scalar(select(ReferralAccount).where(ReferralAccount.invite_code == invite_code))
            if existing_invite is None or existing_invite.user_id == current_user_id():
                break
            suffix += 1
            digest = hashlib.sha1(f"{current_user_id()}:{suffix}".encode("utf-8")).hexdigest()[:10].upper()
            invite_code = f"SEA{digest}"
        session.add(ReferralAccount(user_id=current_user_id(), invite_code=invite_code, invited_count=3, reward_vip_days=7, next_reward_need=5))

    await seed_gifts(session)
    await seed_prompt_templates(session)
    await seed_membership_products(session)
    await seed_content(session)
    await seed_wallet_side_data(session)
    await session.commit()
    await session.refresh(user)
    return user


async def seed_gifts(session: AsyncSession) -> None:
    gifts = [
        ("gift_shell", "贝壳", 10, "贝", "心意", 10),
        ("gift_star", "星光", 30, "星", "心意", 20),
        ("gift_flower", "海花", 52, "花", "浪漫", 30),
        ("gift_bottle", "玻璃瓶", 68, "瓶", "漂流", 40),
        ("gift_moon", "月亮灯", 99, "月", "浪漫", 50),
        ("gift_whale", "小鲸鱼", 188, "鲸", "珍藏", 60),
        ("gift_plane", "星际飞机", 388, "机", "珍藏", 70),
        ("gift_island", "私人小岛", 520, "岛", "珍藏", 80),
        ("gift_crown", "星海皇冠", 999, "冠", "高级", 90),
    ]
    for gift_id, name, price, icon, category, order in gifts:
        existing = await session.get(GiftProduct, gift_id)
        if existing is None:
            session.add(GiftProduct(id=gift_id, name=name, price_coins=price, icon_text=icon, category=category, status="active", sort_order=order, created_at=now()))


async def seed_prompt_templates(session: AsyncSession) -> None:
    if await session.scalar(select(func.count(PromptTemplate.id))) > 0:
        return
    sort_order = 10
    for prompt_id, category, text in TRUTH_QUESTIONS:
        session.add(
            PromptTemplate(
                id=prompt_id,
                prompt_type="truth",
                mode=None,
                category=category,
                text=text,
                meaning=None,
                visibility="private",
                status="active",
                sort_order=sort_order,
                created_at=now(),
            )
        )
        sort_order += 10
    for prompt_id, category, text in DARE_TASKS:
        session.add(
            PromptTemplate(
                id=prompt_id,
                prompt_type="dare",
                mode=None,
                category=category,
                text=text,
                meaning=None,
                visibility="private",
                status="active",
                sort_order=sort_order,
                created_at=now(),
            )
        )
        sort_order += 10
    for prompt_id, mode, text, meaning, visibility in GAME_PROMPTS:
        session.add(
            PromptTemplate(
                id=prompt_id,
                prompt_type="game",
                mode=mode,
                category=mode,
                text=text,
                meaning=meaning,
                visibility=visibility,
                status="active",
                sort_order=sort_order,
                created_at=now(),
            )
        )
        sort_order += 10


async def seed_membership_products(session: AsyncSession) -> None:
    if await session.scalar(select(func.count(MembershipProductConfig.id))) > 0:
        return
    benefits = ["每日次数增加", "会员身份标识", "专属装扮", "历史记录扩容"]
    products = [
        ("vip_month", "月卡会员", "¥18", "all", 10),
        ("vip_season", "季卡会员", "¥45", "all", 20),
        ("vip_year", "年卡会员", "¥128", "all", 30),
    ]
    for product_id, name, price_label, platform, sort_order in products:
        session.add(
            MembershipProductConfig(
                id=product_id,
                name=name,
                price_label=price_label,
                platform=platform,
                benefits_text="\n".join(benefits),
                status="active",
                sort_order=sort_order,
                created_at=now(),
            )
        )


async def seed_content(session: AsyncSession) -> None:
    if await session.scalar(select(func.count(Bottle.id))) == 0:
        seed_bottles = [
            ("bottle_001", CREATOR_IDS["creator_001"], "今天把想说的话写进瓶子里，希望捞到的人刚好也需要一点安静。", "温柔"),
            ("bottle_002", CREATOR_IDS["creator_002"], "那我先把今天整理好，明天再往前走一步。", "晚风"),
            ("bottle_003", CREATOR_IDS["creator_003"], "附近 2km 有一家甜品店，适合不说话地坐一会儿。", "附近"),
            ("bottle_004", CREATOR_IDS["creator_004"], "如果你也刚好睡不着，就把这句话当成今晚的灯。", "夜聊"),
            ("bottle_005", CREATOR_IDS["creator_005"], "有些话不想让熟人看见，但也不想一直憋着。", "树洞"),
            ("bottle_006", CREATOR_IDS["creator_006"], "路灯亮起来的时候，今天好像也被温柔地收尾了。", "视频"),
            ("bottle_007", CREATOR_IDS["creator_007"], "认真回复的人，总会被认真记住。", "认真"),
            ("bottle_008", CREATOR_IDS["creator_008"], "我想找一个能一起玩真心话的人。", "游戏"),
        ]
        for bottle_id, author_id, content, mood in seed_bottles:
            author = await session.get(User, author_id)
            if author is None:
                continue
            session.add(
                Bottle(
                    id=bottle_id,
                    author_id=author.id,
                    author_name=author.nickname,
                    author_avatar_text=author.avatar_text,
                    author_vip=author.is_vip,
                    author_gender=author.gender,
                    author_age_range=author.age_range,
                    author_city=author.city,
                    author_verified=author.face_verified and author.gender_verified,
                    content=content,
                    mood=mood,
                    status="approved",
                    replies=1 if bottle_id == "bottle_001" else 0,
                    target_gender="all",
                    target_scope="all",
                    created_at=now(),
                )
            )

    if await session.scalar(select(func.count(PlazaPost.id))) == 0:
        await create_seed_plaza(session)
    if await session.scalar(select(func.count(TreeholePost.id))) == 0:
        for post_id, author_id, content in [
            ("tree_001", CREATOR_IDS["creator_001"], "有些话不想让熟人看见，但憋在心里又太重了。"),
            ("tree_002", CREATOR_IDS["creator_002"], "今天收到一句很轻的安慰，突然觉得没那么糟。"),
        ]:
            author = await session.get(User, author_id)
            session.add(
                TreeholePost(
                    id=post_id,
                    author_id=author_id,
                    author_name=author.nickname if author else "匿名",
                    author_avatar_text=author.avatar_text if author else "匿",
                    author_gender=author.gender if author else "unknown",
                    author_age_range=author.age_range if author else None,
                    content=content,
                    resonance_count=2,
                    reply_count=1,
                    paid_photo_count=0,
                    status="approved",
                    created_at=now(),
                )
            )
    await create_seed_threads(session)


async def create_seed_plaza(session: AsyncSession) -> None:
    posts = [
        ("plaza_001", CREATOR_IDS["creator_001"], "今日心情", "今晚想收一只认真写的动态，也想把好运分给路过的人。", "image", 9, "同城"),
        ("plaza_002", CREATOR_IDS["creator_003"], "附近动态", "附近 2km 有人分享了今天的晚风和一家新开的甜品店。", "voice", 1, "2.1km"),
        ("plaza_003", CREATOR_IDS["creator_006"], "新人推荐", "拍了一段傍晚路灯亮起来的视频，感觉今天也有一点值得被记住。", "video", 1, "新人"),
    ]
    for post_id, author_id, topic, content, media_type, media_count, distance in posts:
        author = await session.get(User, author_id)
        if author is None:
            continue
        post = PlazaPost(
            id=post_id,
            author_id=author.id,
            author_name=author.nickname,
            icon_text=author.avatar_text or "匿",
            topic=topic,
            content=content,
            media_type=media_type,
            media_count=media_count,
            gender=author.gender,
            verified=author.face_verified and author.gender_verified,
            city=author.city,
            age_range=author.age_range,
            view_count=0,
            like_count=328 if post_id == "plaza_001" else 89,
            comment_count=0,
            comment_preview=None,
            status="approved",
            distance_text=distance,
            created_at=now(),
        )
        session.add(post)
        await session.flush()
        if media_type != "text":
            media_count_to_seed = media_count if media_type == "image" else 1
            for index in range(media_count_to_seed):
                session.add(
                    PlazaMedia(
                        id=f"{post_id}_media_{index + 1}",
                        post_id=post_id,
                        owner_id=author.id,
                        media_type=media_type,
                        url=default_media_url(media_type, post_id, index),
                        storage_key=f"plaza/{post_id}_{index + 1}",
                        mime_type=default_mime(media_type),
                        size_bytes=400000,
                        duration_seconds=5 if media_type == "video" else 2 if media_type == "voice" else None,
                        width=1080 if media_type in {"image", "video"} else None,
                        height=1440 if media_type in {"image", "video"} else None,
                        status="approved",
                        created_at=now(),
                    )
                )
    await add_plaza_comment(session, "plaza_001", current_user_id(), "这条动态很舒服。", False)
    await add_plaza_comment(session, "plaza_001", CREATOR_IDS["creator_002"], "这条只想给发布者看到。", True)
    await add_plaza_comment(session, "plaza_002", CREATOR_IDS["creator_008"], "如果是晚上去，记得点靠窗的位置。", False)


async def create_seed_threads(session: AsyncSession) -> None:
    user = await session.get(User, current_user_id())
    user_name = user.nickname if user else "海风来信"

    async def add_thread(
        *,
        key: str,
        bottle_id: str | None,
        user_b_id: str,
        participant_name: str,
        participant_tag: str,
        related_content: str,
        last_message: str,
        unread_count: int,
        turns: list[dict[str, str]],
        room_mode: str | None = None,
        report_reason: str | None = None,
    ) -> None:
        thread_id = stable_user_seed_id("thread", key)
        if await session.get(ConversationThread, thread_id) is not None:
            return

        thread = ConversationThread(
            id=thread_id,
            bottle_id=bottle_id,
            user_a_id=current_user_id(),
            user_b_id=user_b_id,
            participant_name=participant_name,
            participant_tag=participant_tag,
            bottle_preview=related_content,
            last_message=last_message,
            unread_count=unread_count,
            status="active",
            created_at=now(),
            updated_at=now(),
        )
        session.add(thread)

        room_id: str | None = None
        if room_mode:
            room_id = stable_user_seed_id("room", key)
            session.add(GameRoom(id=room_id, owner_id=current_user_id(), thread_id=thread_id, mode=room_mode, status="open", created_at=now()))

        seed_turns = []
        for index, turn in enumerate(turns, start=1):
            turn_type = turn.get("type", "text")
            seed_turns.append(
                ConversationTurn(
                    id=stable_user_seed_id("turn", f"{key}_{index}"),
                    thread_id=thread_id,
                    sender_id=turn["sender_id"],
                    sender_name=turn["sender_name"],
                    body=turn["body"],
                    turn_type=turn_type,
                    game_room_id=room_id if turn_type == "game_room" else None,
                    created_at=now(),
                )
            )
        session.add_all(seed_turns)

        if report_reason:
            session.add(
                ContentReport(
                    id=stable_user_seed_id("report", key),
                    reporter_id=current_user_id(),
                    target_type="chat",
                    target_id=thread_id,
                    reason=report_reason,
                    status="reviewing",
                    created_at=now(),
                )
            )

    await add_thread(
        key="welcome",
        bottle_id="bottle_001",
        user_b_id=CREATOR_IDS["creator_001"],
        participant_name="匿名海岛客",
        participant_tag="漂流瓶回应",
        related_content="今天把想说的话写进瓶子里，希望捞到的人刚好也需要一点安静。",
        last_message="我也有过类似的夜晚，看到这句的时候刚好安静下来。",
        unread_count=1,
        turns=[
            {"sender_id": CREATOR_IDS["creator_001"], "sender_name": "匿名海岛客", "body": "今天把想说的话写进瓶子里，希望捞到的人刚好也需要一点安静。"},
            {"sender_id": current_user_id(), "sender_name": user_name, "body": "我收到了。今晚确实需要一点安静，谢谢你。"},
            {"sender_id": CREATOR_IDS["creator_001"], "sender_name": "匿名海岛客", "body": "我也有过类似的夜晚，看到这句的时候刚好安静下来。"},
        ],
    )
    await add_thread(
        key="treehole_support",
        bottle_id=None,
        user_b_id=CREATOR_IDS["creator_005"],
        participant_name="小满",
        participant_tag="树洞倾诉",
        related_content="树洞：有些话不想让熟人看见，但憋在心里又太重了。",
        last_message="先把今晚过完，明天再决定要不要继续聊。",
        unread_count=0,
        turns=[
            {"sender_id": CREATOR_IDS["creator_005"], "sender_name": "小满", "body": "我在树洞里看到你的回复，想认真说声谢谢。"},
            {"sender_id": current_user_id(), "sender_name": user_name, "body": "不用急着好起来，先把今晚过完就好。"},
            {"sender_id": CREATOR_IDS["creator_005"], "sender_name": "小满", "body": "先把今晚过完，明天再决定要不要继续聊。"},
        ],
    )
    await add_thread(
        key="plaza_comment",
        bottle_id=None,
        user_b_id=CREATOR_IDS["creator_003"],
        participant_name="北岸",
        participant_tag="广场互动",
        related_content="广场：附近 2km 有人分享了今天的晚风和一家新开的甜品店。",
        last_message="如果去那家店，建议坐靠窗的位置。",
        unread_count=0,
        turns=[
            {"sender_id": current_user_id(), "sender_name": user_name, "body": "你说的甜品店是在河边那家吗？"},
            {"sender_id": CREATOR_IDS["creator_003"], "sender_name": "北岸", "body": "是的，晚上人少一点。"},
            {"sender_id": CREATOR_IDS["creator_003"], "sender_name": "北岸", "body": "如果去那家店，建议坐靠窗的位置。"},
        ],
    )
    await add_thread(
        key="game_room_watch",
        bottle_id=None,
        user_b_id=CREATOR_IDS["creator_007"],
        participant_name="南风",
        participant_tag="游戏房间",
        related_content="真心话大冒险房间：公开破冰局",
        last_message="请按房间规则来，别刷屏，也不要约线下。",
        unread_count=2,
        room_mode="mixed",
        report_reason="chat_risk:刷屏,约线下",
        turns=[
            {"sender_id": current_user_id(), "sender_name": user_name, "body": "创建了真心话大冒险房间，邀请对方一起玩", "type": "game_room"},
            {"sender_id": CREATOR_IDS["creator_007"], "sender_name": "南风", "body": "我先选真心话，问题可以轻一点。"},
            {"sender_id": current_user_id(), "sender_name": user_name, "body": "可以，公开房间不问隐私。"},
            {"sender_id": CREATOR_IDS["creator_007"], "sender_name": "南风", "body": "有人开始刷屏，还想约线下，先提醒一下。"},
            {"sender_id": current_user_id(), "sender_name": user_name, "body": "请按房间规则来，别刷屏，也不要约线下。"},
        ],
    )
    await add_thread(
        key="game_room_clean",
        bottle_id=None,
        user_b_id=CREATOR_IDS["creator_008"],
        participant_name="阿树",
        participant_tag="游戏房间",
        related_content="真心话房间：轻量聊天局",
        last_message="这个问题刚好适合今天。",
        unread_count=0,
        room_mode="truth",
        turns=[
            {"sender_id": current_user_id(), "sender_name": user_name, "body": "创建了真心话房间，邀请对方一起玩", "type": "game_room"},
            {"sender_id": CREATOR_IDS["creator_008"], "sender_name": "阿树", "body": "我想回答一个关于最近开心瞬间的问题。"},
            {"sender_id": current_user_id(), "sender_name": user_name, "body": "这个问题刚好适合今天。"},
        ],
    )

    if await session.get(MessageNotification, stable_user_seed_id("msg", "welcome")) is None:
        session.add(
            MessageNotification(
                id=stable_user_seed_id("msg", "welcome"),
                user_id=current_user_id(),
                title="漂流瓶有新回应",
                body="匿名海岛客回复了你的瓶子。",
                unread=True,
                business_type="bottle",
                business_id="bottle_001",
                created_at=now(),
            )
        )


async def seed_wallet_side_data(session: AsyncSession) -> None:
    if await session.scalar(select(func.count(CoinLedger.id)).where(CoinLedger.user_id == current_user_id())) == 0:
        session.add_all(
            [
                CoinLedger(id=stable_user_seed_id("ledger", "private_photo_income"), user_id=current_user_id(), title="私密照片被查看", amount=30, coin_bucket="earned", withdrawable=True, business_type="private_photo", business_id="photo_001", created_at=now()),
                CoinLedger(id=stable_user_seed_id("ledger", "recharge_seed"), user_id=current_user_id(), title="充值金币", amount=200, coin_bucket="recharge", withdrawable=False, business_type="recharge", business_id="pay_seed_001", created_at=now()),
            ]
        )
    if await session.scalar(select(func.count(PrivatePhotoAsset.id))) == 0:
        session.add_all(
            [
                PrivatePhotoAsset(id="photo_001", owner_id=CREATOR_IDS["creator_001"], owner_name="海岛来信", title="今日海边碎片", cover_tone="mint", price_coins=30, status="approved", purchased_by_user_ids="", created_at=now()),
                PrivatePhotoAsset(id="photo_002", owner_id=CREATOR_IDS["creator_002"], owner_name="晚风", title="只给认真回应的人看", cover_tone="rose", price_coins=20, status="approved", purchased_by_user_ids="", created_at=now()),
            ]
        )
    if await session.scalar(select(func.count(BlacklistEntry.id)).where(BlacklistEntry.owner_id == current_user_id())) == 0:
        session.add(BlacklistEntry(id=stable_user_seed_id("block", "bad_user_001"), owner_id=current_user_id(), blocked_user_id=CREATOR_IDS["bad_user_001"], nickname="无礼访客", reason="骚扰私信", status="blocked", blocked_at=now()))


async def add_notification(session: AsyncSession, title: str, body: str, business_type: str | None = None, business_id: str | None = None) -> None:
    session.add(MessageNotification(id=new_id("msg"), user_id=current_user_id(), title=title, body=body, unread=True, business_type=business_type, business_id=business_id, created_at=now()))


async def add_user_notification(session: AsyncSession, user_id: str, title: str, body: str, business_type: str | None = None, business_id: str | None = None) -> None:
    session.add(MessageNotification(id=new_id("msg"), user_id=user_id, title=title, body=body, unread=True, business_type=business_type, business_id=business_id, created_at=now()))


async def get_current_user(session: AsyncSession) -> User:
    user = await ensure_seed_data(session)
    latest_restriction = await session.scalar(
        select(AdminUserRestriction)
        .where(AdminUserRestriction.user_id == user.id)
        .order_by(desc(AdminUserRestriction.updated_at))
        .limit(1)
    )
    if latest_restriction and latest_restriction.status == "blocked":
        if latest_restriction.blocked_until is None or latest_restriction.blocked_until > now():
            raise HTTPException(
                status_code=403,
                detail={"code": "USER_BLOCKED", "message": "账号已被封禁，暂时无法使用当前账号。"},
            )
        if user.status == "blocked":
            user.status = "active"
            await session.commit()
    if user.status == "blocked":
        raise HTTPException(
            status_code=403,
            detail={"code": "USER_BLOCKED", "message": "账号已被封禁，暂时无法使用当前账号。"},
        )
    if user.status not in {"active", "limited", "blocked"}:
        raise HTTPException(status_code=403, detail={"code": "USER_STATUS_INVALID", "message": "账号状态异常。"})
    return user


def _coerce_blocked_until(blocked_until: str | None, block_days: int | None) -> datetime | None:
    if blocked_until:
        try:
            candidate = datetime.fromisoformat(blocked_until.replace("Z", "+00:00"))
        except ValueError as exc:
            raise HTTPException(status_code=422, detail="INVALID_BLOCKED_UNTIL") from exc
        if candidate.tzinfo is None:
            return candidate.replace(tzinfo=UTC)
        return candidate.astimezone(UTC)
    if block_days is None:
        return None
    if block_days <= 0:
        return None
    return now() + timedelta(days=block_days)


async def get_status(session: AsyncSession) -> MeStatus:
    user = await get_current_user(session)
    ad_config = await get_admin_reward_config(session)
    rows = (await session.execute(select(QuotaBalance).where(QuotaBalance.user_id == user.id))).scalars().all()
    quotas = {
        QuotaType(row.quota_type): QuotaItem(
            type=QuotaType(row.quota_type),
            label=BASE_QUOTAS[QuotaType(row.quota_type)][0],
            base=row.base,
            vip_bonus=row.vip_bonus,
            ad_bonus=row.ad_bonus,
            used=row.used,
            remaining=row.remaining,
        )
        for row in rows
        if row.quota_type in {item.value for item in QuotaType}
    }
    latest_checkin = await session.scalar(select(CheckinRecord).where(CheckinRecord.user_id == user.id).order_by(desc(CheckinRecord.created_at)).limit(1))
    last_ad = await session.scalar(select(AdRewardSession).where(AdRewardSession.user_id == user.id).order_by(desc(AdRewardSession.created_at)).limit(1))
    cooldown_seconds = 0
    if last_ad and last_ad.status == "settled" and last_ad.settled_at:
        settled_at = last_ad.settled_at
        if settled_at.tzinfo is None:
            settled_at = settled_at.replace(tzinfo=UTC)
        else:
            settled_at = settled_at.astimezone(UTC)
        elapsed = (now() - settled_at).total_seconds()
        cooldown_seconds = max(0, int(ad_config.ad_cooldown_minutes * 60 - elapsed))
    return MeStatus(
        user=to_user_profile(user),
        quotas=quotas,
        ad_reward=AdRewardState(
            can_watch=cooldown_seconds == 0,
            cooldown_seconds=cooldown_seconds,
            cooldown_minutes=ad_config.ad_cooldown_minutes,
            reward_per_quota=ad_config.ad_reward_per_quota,
            active_session_id=last_ad.id if last_ad and last_ad.status == "prepared" else None,
            display_type=ad_config.ad_display_type,
            provider=ad_config.ad_provider,
            placement_id=ad_config.ad_placement_id,
            title=ad_config.ad_title,
            description=ad_config.ad_description,
            media_url=ad_config.ad_media_url,
            click_url=ad_config.ad_click_url,
            countdown_seconds=ad_config.ad_countdown_seconds,
            mini_program_app_id=ad_config.mini_program_app_id,
            mini_program_path=ad_config.mini_program_path,
        ),
        checkin=CheckinState(
            checked_today=latest_checkin.checkin_date == date.today().isoformat() if latest_checkin else False,
            streak_days=latest_checkin.streak_days if latest_checkin else 0,
            week_rewards=CHECKIN_REWARDS,
            current_week_index=(latest_checkin.streak_days if latest_checkin else 0) % len(CHECKIN_REWARDS),
            last_reward=latest_checkin.reward_count if latest_checkin else None,
        ),
    )


async def list_user_record_summaries(session: AsyncSession) -> list[UserRecordSummaryItem]:
    await get_current_user(session)
    user_id = current_user_id()
    bottle_count = (await session.scalar(select(func.count(Bottle.id)).where(Bottle.author_id == user_id)) or 0) + (
        await session.scalar(select(func.count(BottleReply.id)).where(BottleReply.author_id == user_id)) or 0
    )
    treehole_count = (
        await session.scalar(select(func.count(TreeholePost.id)).where(TreeholePost.author_id == user_id)) or 0
    ) + (await session.scalar(select(func.count(TreeholeReply.id)).where(TreeholeReply.author_id == user_id)) or 0) + (
        await session.scalar(select(func.count(TreeholeReaction.id)).where(TreeholeReaction.user_id == user_id)) or 0
    )
    truth_count = await session.scalar(select(func.count(UserActivityRecord.id)).where(UserActivityRecord.user_id == user_id, UserActivityRecord.record_type == "truth")) or 0
    dare_count = await session.scalar(select(func.count(UserActivityRecord.id)).where(UserActivityRecord.user_id == user_id, UserActivityRecord.record_type == "dare")) or 0
    game_count = (await session.scalar(select(func.count(UserActivityRecord.id)).where(UserActivityRecord.user_id == user_id, UserActivityRecord.record_type == "game")) or 0) + (
        await session.scalar(select(func.count(GameRoom.id)).where(GameRoom.owner_id == user_id)) or 0
    )
    report_count = await session.scalar(select(func.count(ContentReport.id)).where(ContentReport.reporter_id == user_id)) or 0
    return [
        UserRecordSummaryItem(type="bottle", title="我的瓶子", desc="已投递和已回应的瓶子", count=bottle_count),
        UserRecordSummaryItem(type="treehole", title="我的树洞", desc="发布、共鸣和回复记录", count=treehole_count),
        UserRecordSummaryItem(type="truth", title="真心话记录", desc="公开和私密真心话", count=truth_count),
        UserRecordSummaryItem(type="dare", title="大冒险记录", desc="完成和保存的大冒险", count=dare_count),
        UserRecordSummaryItem(type="game", title="游戏记录", desc="创建房间和保存玩法", count=game_count),
        UserRecordSummaryItem(type="report", title="举报记录", desc="安全处理进度", count=report_count),
    ]


async def create_user_activity_record(session: AsyncSession, payload: UserActivityRecordCreateRequest) -> UserActivityRecordOut:
    await get_current_user(session)
    row = UserActivityRecord(
        id=new_id("activity"),
        user_id=current_user_id(),
        record_type=payload.record_type,
        title=payload.title.strip(),
        content=payload.content.strip(),
        visibility=payload.visibility,
        source_type=payload.source_type,
        source_id=payload.source_id,
        created_at=now(),
    )
    session.add(row)
    await session.commit()
    return UserActivityRecordOut(
        id=row.id,
        record_type=row.record_type,
        title=row.title,
        content=row.content,
        visibility=row.visibility,
        source_type=row.source_type,
        source_id=row.source_id,
        created_at=iso(row.created_at),
    )


async def list_truth_questions(session: AsyncSession) -> list[TruthQuestionOut]:
    await get_current_user(session)
    rows = (await session.execute(select(PromptTemplate).where(PromptTemplate.prompt_type == "truth", PromptTemplate.status == "active").order_by(PromptTemplate.sort_order))).scalars().all()
    return [TruthQuestionOut(id=row.id, category=row.category, text=row.text) for row in rows]


async def random_truth_question(session: AsyncSession) -> TruthQuestionOut:
    rows = await list_truth_questions(session)
    if not rows:
        raise HTTPException(status_code=404, detail="TRUTH_PROMPT_NOT_FOUND")
    return choice(rows)


async def list_dare_tasks(session: AsyncSession) -> list[DareTaskOut]:
    await get_current_user(session)
    rows = (await session.execute(select(PromptTemplate).where(PromptTemplate.prompt_type == "dare", PromptTemplate.status == "active").order_by(PromptTemplate.sort_order))).scalars().all()
    return [DareTaskOut(id=row.id, category=row.category, text=row.text) for row in rows]


async def random_dare_task(session: AsyncSession) -> DareTaskOut:
    rows = await list_dare_tasks(session)
    if not rows:
        raise HTTPException(status_code=404, detail="DARE_PROMPT_NOT_FOUND")
    return choice(rows)


async def random_game_prompt(session: AsyncSession, mode: str) -> GamePromptOut:
    await get_current_user(session)
    rows = (
        await session.execute(
            select(PromptTemplate).where(PromptTemplate.prompt_type == "game", PromptTemplate.mode == mode, PromptTemplate.status == "active")
        )
    ).scalars().all()
    if not rows:
        raise HTTPException(status_code=404, detail="GAME_PROMPT_NOT_FOUND")
    row = choice(rows)
    return GamePromptOut(id=row.id, mode=row.mode, text=row.text, meaning=row.meaning or "自定义玩法内容", visibility=row.visibility or "所有参与者可见")


def to_user_profile(user: User) -> UserProfile:
    vip_expires_at = None
    if user.is_vip:
        vip_days = {"monthly": 30, "season": 90, "yearly": 365}.get(user.vip_level, 30)
        vip_expires_at = iso(user.created_at + timedelta(days=vip_days))
    return UserProfile(
        id=user.id,
        nickname=user.nickname,
        avatar_text=user.avatar_text or "海",
        avatar_url=resolved_avatar_url(user, user.id),
        platform=user.platform if user.platform in {"wechat", "ios", "android", "h5"} else "h5",
        is_vip=user.is_vip,
        vip_level=user.vip_level if user.vip_level in {"none", "monthly", "season", "yearly"} else "none",
        vip_expires_at=vip_expires_at,
        drift_coins=user.drift_coins,
        gender=user.gender if user.gender in {"female", "male", "unknown"} else "unknown",
        age_range=user.age_range,
        city=user.city,
        face_verified=user.face_verified,
        gender_verified=user.gender_verified,
        charm_value=user.charm_value,
    )


async def update_profile(session: AsyncSession, payload: UserProfileUpdateRequest) -> UserProfile:
    user = await get_current_user(session)
    patch = payload.model_dump(exclude_unset=True)
    if "nickname" in patch and patch["nickname"] is not None:
        nickname = patch["nickname"].strip()
        if not nickname:
            raise HTTPException(status_code=422, detail="EMPTY_NICKNAME")
        user.nickname = nickname
    if "avatar_text" in patch:
        user.avatar_text = patch["avatar_text"]
    if "avatar_url" in patch:
        user.avatar_url = patch["avatar_url"]
    if "gender" in patch and patch["gender"] is not None:
        user.gender = patch["gender"]
    if "city" in patch:
        user.city = patch["city"]
    if "age_range" in patch:
        user.age_range = patch["age_range"]
    for bottle in (await session.execute(select(Bottle).where(Bottle.author_id == user.id))).scalars().all():
        bottle.author_name = user.nickname
        bottle.author_avatar_text = user.avatar_text
        bottle.author_vip = user.is_vip
        bottle.author_gender = user.gender
        bottle.author_age_range = user.age_range
        bottle.author_city = user.city
        bottle.author_verified = user.face_verified and user.gender_verified
    for post in (await session.execute(select(PlazaPost).where(PlazaPost.author_id == user.id))).scalars().all():
        post.author_name = user.nickname
        post.icon_text = user.avatar_text or "海"
        post.gender = user.gender
        post.city = user.city
        post.age_range = user.age_range
        post.verified = user.face_verified and user.gender_verified
    for comment in (await session.execute(select(PlazaComment).where(PlazaComment.author_id == user.id))).scalars().all():
        comment.author_name = user.nickname
        comment.icon_text = user.avatar_text or "匿"
        comment.author_gender = user.gender
        comment.author_age_range = user.age_range
        comment.author_verified = user.face_verified and user.gender_verified
        comment.author_city = user.city
    for tree in (await session.execute(select(TreeholePost).where(TreeholePost.author_id == user.id))).scalars().all():
        tree.author_name = user.nickname
        tree.author_avatar_text = user.avatar_text
        tree.author_avatar_url = user.avatar_url
        tree.author_gender = user.gender
        tree.author_age_range = user.age_range
    for photo in (await session.execute(select(PrivatePhotoAsset).where(PrivatePhotoAsset.owner_id == user.id))).scalars().all():
        photo.owner_name = user.nickname
    for block in (await session.execute(select(BlacklistEntry).where(BlacklistEntry.blocked_user_id == user.id))).scalars().all():
        block.nickname = user.nickname
    for thread in (await session.execute(select(ConversationThread).where(ConversationThread.user_b_id == user.id))).scalars().all():
        thread.participant_name = user.nickname
    for turn in (await session.execute(select(ConversationTurn).where(ConversationTurn.sender_id == user.id))).scalars().all():
        turn.sender_name = user.nickname
    await session.commit()
    await session.refresh(user)
    return to_user_profile(user)


async def consume_quota(session: AsyncSession, quota_type: QuotaType, business_id: str) -> QuotaItem:
    await get_current_user(session)
    row = await session.scalar(select(QuotaBalance).where(QuotaBalance.user_id == current_user_id(), QuotaBalance.quota_type == quota_type.value))
    if row is None:
        raise HTTPException(status_code=404, detail="QUOTA_NOT_FOUND")
    consumed = await session.scalar(
        select(CoinLedger).where(
            CoinLedger.user_id == current_user_id(),
            CoinLedger.business_type == f"quota:{quota_type.value}",
            CoinLedger.business_id == business_id,
        )
    )
    if consumed is not None:
        return quota_to_schema(row)
    if row.remaining <= 0:
        raise HTTPException(status_code=409, detail="QUOTA_NOT_ENOUGH")
    row.used += 1
    row.remaining -= 1
    row.updated_at = now()
    session.add(CoinLedger(id=new_id("quota_log"), user_id=current_user_id(), title=f"使用{BASE_QUOTAS[quota_type][0]}", amount=0, coin_bucket="earned", withdrawable=False, business_type=f"quota:{quota_type.value}", business_id=business_id, created_at=now()))
    await session.commit()
    return quota_to_schema(row)


def quota_to_schema(row: QuotaBalance) -> QuotaItem:
    quota_type = QuotaType(row.quota_type)
    return QuotaItem(type=quota_type, label=BASE_QUOTAS[quota_type][0], base=row.base, vip_bonus=row.vip_bonus, ad_bonus=row.ad_bonus, used=row.used, remaining=row.remaining)


async def checkin_today(session: AsyncSession) -> CheckinState:
    await get_current_user(session)
    today = date.today().isoformat()
    existing = await session.scalar(select(CheckinRecord).where(CheckinRecord.user_id == current_user_id(), CheckinRecord.checkin_date == today))
    if existing is None:
        previous = await session.scalar(select(CheckinRecord).where(CheckinRecord.user_id == current_user_id()).order_by(desc(CheckinRecord.created_at)).limit(1))
        streak = (previous.streak_days if previous else 0) + 1
        reward = CHECKIN_REWARDS[(streak - 1) % len(CHECKIN_REWARDS)]
        existing = CheckinRecord(id=new_id("checkin"), user_id=current_user_id(), checkin_date=today, reward_count=reward, streak_days=streak, created_at=now())
        session.add(existing)
        for quota in (await session.execute(select(QuotaBalance).where(QuotaBalance.user_id == current_user_id()))).scalars().all():
            quota.ad_bonus += reward
            quota.remaining += reward
            quota.updated_at = now()
        await add_notification(session, "签到成功", f"今日签到奖励所有次数 +{reward}", "checkin", existing.id)
        await session.commit()
    return CheckinState(checked_today=True, streak_days=existing.streak_days, week_rewards=CHECKIN_REWARDS, current_week_index=existing.streak_days % len(CHECKIN_REWARDS), last_reward=existing.reward_count)


async def prepare_ad_reward(session: AsyncSession) -> str:
    await get_current_user(session)
    ad_state = (await get_status(session)).ad_reward
    if not ad_state.can_watch:
        raise HTTPException(
            status_code=409,
            detail={
                "code": "AD_REWARD_COOLDOWN",
                "message": "Reward video is cooling down",
                "details": {"cooldown_seconds": ad_state.cooldown_seconds},
            },
        )
    reward = AdRewardSession(
        id=new_id("ad"),
        user_id=current_user_id(),
        reward_per_quota=ad_state.reward_per_quota,
        reward_coin=1,
        status="prepared",
        created_at=now(),
    )
    session.add(reward)
    await session.commit()
    return reward.id


async def commit_ad_reward(session: AsyncSession, reward_session_id: str, completed: bool) -> MeStatus:
    await get_current_user(session)
    reward = await session.get(AdRewardSession, reward_session_id)
    if reward and reward.user_id != current_user_id():
        raise HTTPException(status_code=404, detail="AD_REWARD_SESSION_NOT_FOUND")
    if reward and completed and reward.status == "prepared":
        reward.status = "settled"
        reward.settled_at = now()
        for quota in (await session.execute(select(QuotaBalance).where(QuotaBalance.user_id == current_user_id()))).scalars().all():
            quota.ad_bonus += reward.reward_per_quota
            quota.remaining += reward.reward_per_quota
            quota.updated_at = now()
        wallet = await session.get(WalletAccount, current_user_id())
        if wallet:
            wallet.recharge_coins += reward.reward_coin
            wallet.updated_at = now()
        session.add(CoinLedger(id=new_id("ledger"), user_id=current_user_id(), title="看视频奖励金币", amount=reward.reward_coin, coin_bucket="recharge", withdrawable=False, business_type="ad_reward", business_id=reward.id, created_at=now()))
        await add_notification(session, "看视频奖励已到账", f"金币 +{reward.reward_coin}，所有次数 +{reward.reward_per_quota}", "ad_reward", reward.id)
        await session.commit()
    return await get_status(session)


async def to_bottle(session: AsyncSession, row: Bottle, is_following: bool = False, friend_requested: bool = False) -> BottleOut:
    author = await session.get(User, row.author_id)
    return BottleOut(
        id=row.id,
        author_id=row.author_id,
        author_name=author.nickname if author else row.author_name,
        author_avatar_text=author.avatar_text if author else row.author_avatar_text,
        author_avatar_url=author.avatar_url if author else None,
        author_vip=author.is_vip if author else row.author_vip,
        author_gender=(author.gender if author else row.author_gender) if (author.gender if author else row.author_gender) in {"female", "male", "unknown"} else "unknown",
        author_age_range=author.age_range if author else row.author_age_range,
        author_city=author.city if author else row.author_city,
        author_verified=(author.face_verified and author.gender_verified) if author else row.author_verified,
        content=row.content,
        mood=row.mood,
        status=row.status,
        replies=row.replies,
        target_gender=row.target_gender if row.target_gender in {"all", "female", "male"} else "all",
        target_scope=row.target_scope if row.target_scope in {"all", "same_city", "nearby"} else "all",
        is_following=is_following,
        friend_requested=friend_requested,
        created_at=iso(row.created_at),
    )


async def bottle_flags(session: AsyncSession, author_id: str) -> tuple[bool, bool]:
    followed = await session.scalar(select(Follow).where(Follow.follower_id == current_user_id(), Follow.target_user_id == author_id))
    requested = await session.scalar(select(FriendRequest).where(FriendRequest.requester_id == current_user_id(), FriendRequest.target_user_id == author_id))
    return followed is not None, requested is not None


async def list_bottles(session: AsyncSession) -> list[BottleOut]:
    await get_current_user(session)
    rows = (await session.execute(select(Bottle).where(Bottle.status == "approved").order_by(desc(Bottle.created_at)))).scalars().all()
    result = []
    for row in rows:
        result.append(await to_bottle(session, row, *(await bottle_flags(session, row.author_id))))
    return result


async def random_bottle(session: AsyncSession, city: str | None = None, gender: str | None = None, age_range: str | None = None) -> BottleOut:
    await get_current_user(session)
    rows = (await session.execute(select(Bottle).where(Bottle.status == "approved", Bottle.author_id != current_user_id()))).scalars().all()
    gender_value = normalize_gender(gender)
    if city in {"同城", "杭州"}:
        rows = [item for item in rows if item.author_city == "杭州"]
    if gender_value:
        rows = [item for item in rows if item.author_gender == gender_value]
    if age_range and age_range not in {"全部", "all"}:
        rows = [item for item in rows if item.author_age_range == age_range]
    if not rows:
        raise HTTPException(status_code=404, detail="NO_MATCHED_BOTTLE")
    used_count = await session.scalar(
        select(func.count(CoinLedger.id)).where(
            CoinLedger.user_id == current_user_id(),
            CoinLedger.business_type == f"quota:{QuotaType.fish_bottle.value}",
        )
    )
    picked = sorted(rows, key=lambda item: item.created_at)[(used_count or 0) % len(rows)]
    await consume_quota(session, QuotaType.fish_bottle, new_id("fish"))
    return await to_bottle(session, picked, *(await bottle_flags(session, picked.author_id)))


async def create_bottle(session: AsyncSession, content: str, target_gender: str = "all", target_scope: str = "all") -> BottleOut:
    user = await get_current_user(session)
    body = content.strip()
    if not body:
        raise HTTPException(status_code=422, detail="EMPTY_BOTTLE_CONTENT")
    await consume_quota(session, QuotaType.throw_bottle, new_id("throw"))
    row = Bottle(id=new_id("bottle"), author_id=user.id, author_name=user.nickname, author_avatar_text=user.avatar_text, author_vip=user.is_vip, author_gender=user.gender, author_age_range=user.age_range, author_city=user.city, author_verified=user.face_verified and user.gender_verified, content=body, mood="漂流", status="approved", replies=0, target_gender=target_gender, target_scope=target_scope, created_at=now())
    session.add(row)
    await add_notification(session, "瓶子已漂出", "你的瓶子已经进入漂流池。", "bottle", row.id)
    await session.commit()
    return await to_bottle(session, row)


async def reply_bottle(session: AsyncSession, bottle_id: str, content: str) -> None:
    user = await get_current_user(session)
    bottle = await session.get(Bottle, bottle_id)
    if bottle is None:
        raise HTTPException(status_code=404, detail="BOTTLE_NOT_FOUND")
    bottle.replies += 1
    session.add(BottleReply(id=new_id("reply"), bottle_id=bottle_id, author_id=user.id, content=content.strip(), status="approved", created_at=now()))
    thread = await ensure_thread_for_bottle(session, bottle)
    session.add(ConversationTurn(id=new_id("turn"), thread_id=thread.id, sender_id=user.id, sender_name=user.nickname, body=content.strip(), turn_type="text", created_at=now()))
    thread.last_message = content.strip()
    thread.updated_at = now()
    await add_notification(session, "已发送回应", "你的回应已经进入聊天列表。", "bottle", bottle_id)
    await session.commit()


async def ensure_thread_for_bottle(session: AsyncSession, bottle: Bottle) -> ConversationThread:
    thread = await session.scalar(select(ConversationThread).where(ConversationThread.bottle_id == bottle.id, ConversationThread.user_a_id == current_user_id()))
    if thread is None:
        thread = ConversationThread(id=new_id("thread"), bottle_id=bottle.id, user_a_id=current_user_id(), user_b_id=bottle.author_id, participant_name=bottle.author_name, participant_tag="漂流瓶回应", bottle_preview=bottle.content[:160], last_message=bottle.content[:160], unread_count=0, status="active", created_at=now(), updated_at=now())
        session.add(thread)
    return thread


def random_prompt() -> str:
    return choice([
        "如果今晚有人刚好看到你，你想让对方知道什么？",
        "写一句你不想发朋友圈但很想被听见的话。",
        "把今天最柔软或最糟糕的一瞬间放进瓶子里。",
    ])


def to_treehole(row: TreeholePost) -> TreeholePostOut:
    return TreeholePostOut(id=row.id, author_id=row.author_id, author_name=row.author_name, author_avatar_text=row.author_avatar_text or "匿", author_avatar_url=row.author_avatar_url, author_gender=row.author_gender if row.author_gender in {"female", "male", "unknown"} else "unknown", author_age_range=row.author_age_range, content=row.content, resonance_count=row.resonance_count, reply_count=row.reply_count, paid_photo_count=row.paid_photo_count, status=row.status, created_at=iso(row.created_at))


async def treehole_feed(session: AsyncSession) -> list[TreeholePostOut]:
    await get_current_user(session)
    rows = (await session.execute(select(TreeholePost).where(TreeholePost.status == "approved").order_by(desc(TreeholePost.created_at)))).scalars().all()
    return [to_treehole(row) for row in rows]


async def create_treehole(session: AsyncSession, content: str) -> TreeholePostOut:
    user = await get_current_user(session)
    await consume_quota(session, QuotaType.treehole_post, new_id("treehole"))
    row = TreeholePost(id=new_id("tree"), author_id=user.id, author_name=user.nickname, author_avatar_text=user.avatar_text, author_avatar_url=user.avatar_url, author_gender=user.gender, author_age_range=user.age_range, content=content.strip(), resonance_count=0, reply_count=0, paid_photo_count=0, status="approved", created_at=now())
    session.add(row)
    await add_notification(session, "树洞已发布", "你的树洞已经进入游戏星球。", "treehole", row.id)
    await session.commit()
    return to_treehole(row)


async def react_treehole(session: AsyncSession, post_id: str) -> TreeholePostOut:
    await get_current_user(session)
    post = await session.get(TreeholePost, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="TREEHOLE_NOT_FOUND")
    exists = await session.scalar(select(TreeholeReaction).where(TreeholeReaction.post_id == post_id, TreeholeReaction.user_id == current_user_id(), TreeholeReaction.reaction_type == "resonate"))
    if exists is None:
        post.resonance_count += 1
        session.add(TreeholeReaction(id=new_id("reaction"), post_id=post_id, user_id=current_user_id(), reaction_type="resonate", created_at=now()))
        await session.commit()
    return to_treehole(post)


async def reply_treehole(session: AsyncSession, post_id: str, content: str) -> TreeholePostOut:
    await get_current_user(session)
    post = await session.get(TreeholePost, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="TREEHOLE_NOT_FOUND")
    post.reply_count += 1
    session.add(TreeholeReply(id=new_id("tree_reply"), post_id=post_id, author_id=current_user_id(), content=content.strip(), status="approved", created_at=now()))
    await session.commit()
    return to_treehole(post)


def normalize_gender(value: str | None) -> str | None:
    if value in {"女", "female", "F"}:
        return "female"
    if value in {"男", "male", "M"}:
        return "male"
    return None


def to_media(row: PlazaMedia) -> PlazaMediaOut:
    return PlazaMediaOut(id=row.id, post_id=row.post_id, owner_id=row.owner_id, media_type=row.media_type, url=row.url, storage_key=row.storage_key, mime_type=row.mime_type, size_bytes=row.size_bytes, duration_seconds=row.duration_seconds, width=row.width, height=row.height, created_at=iso(row.created_at))


async def post_media(session: AsyncSession, post_id: str) -> list[PlazaMediaOut]:
    rows = (await session.execute(select(PlazaMedia).where(PlazaMedia.post_id == post_id, PlazaMedia.status == "approved"))).scalars().all()
    return [to_media(row) for row in rows]


async def to_plaza(session: AsyncSession, row: PlazaPost) -> PlazaPostOut:
    liked = await session.scalar(select(PlazaLike).where(PlazaLike.post_id == row.id, PlazaLike.user_id == current_user_id()))
    author = await session.get(User, row.author_id)
    return PlazaPostOut(id=row.id, author_id=row.author_id, author_name=author.nickname if author else row.author_name, icon_text=(author.avatar_text or "海") if author else row.icon_text, icon_url=author.avatar_url if author else None, topic=row.topic, content=row.content, media_type=row.media_type, media_count=row.media_count, gender=(author.gender if author else row.gender), verified=(author.face_verified and author.gender_verified) if author else row.verified, city=(author.city if author else row.city), age_range=(author.age_range if author else row.age_range), view_count=row.view_count, like_count=row.like_count, liked_by_current_user=liked is not None, comment_count=row.comment_count, comment_preview=row.comment_preview, media=await post_media(session, row.id), distance_text=row.distance_text, created_at=iso(row.created_at))


async def list_plaza(session: AsyncSession, city: str | None = None, gender: str | None = None, age_range: str | None = None) -> list[PlazaPostOut]:
    await get_current_user(session)
    stmt = select(PlazaPost).where(PlazaPost.status == "approved").order_by(desc(PlazaPost.created_at))
    rows = (await session.execute(stmt)).scalars().all()
    normalized_gender = normalize_gender(gender)
    if city and city not in {"全国", "all"}:
        rows = [row for row in rows if row.city == city]
    if normalized_gender:
        rows = [row for row in rows if row.gender == normalized_gender]
    if age_range and age_range not in {"全部", "all"}:
        rows = [row for row in rows if age_ranges_overlap(row.age_range, age_range)]
    for row in rows:
        row.view_count += 1
    await session.commit()
    return [await to_plaza(session, row) for row in rows]


async def get_plaza(session: AsyncSession, post_id: str) -> PlazaPostOut:
    await get_current_user(session)
    row = await session.get(PlazaPost, post_id)
    if row is None:
        raise HTTPException(status_code=404, detail="PLAZA_POST_NOT_FOUND")
    return await to_plaza(session, row)


def parse_age_range(value: str | None) -> tuple[int, int] | None:
    if not value or value in {"全部", "all"}:
        return None
    normalized = value.replace("+", "-80")
    parts = normalized.split("-", 1)
    if len(parts) != 2:
        return None
    try:
        left = int(parts[0])
        right = int(parts[1])
    except ValueError:
        return None
    return min(left, right), max(left, right)


def age_ranges_overlap(left: str | None, right: str | None) -> bool:
    left_range = parse_age_range(left)
    right_range = parse_age_range(right)
    if right_range is None:
        return True
    if left_range is None:
        return False
    return left_range[1] >= right_range[0] and left_range[0] <= right_range[1]


def default_media_url(media_type: str, post_id: str, index: int = 0) -> str:
    if media_type == "voice":
        return "https://interactive-examples.mdn.mozilla.net/media/cc0-audio/t-rex-roar.mp3"
    if media_type == "video":
        return "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4"
    return f"https://picsum.photos/seed/{post_id}-{index}/900/1200"


def default_mime(media_type: str) -> str:
    if media_type == "voice":
        return "audio/mpeg"
    if media_type == "video":
        return "video/mp4"
    return "image/jpeg"


async def create_plaza(session: AsyncSession, content: str, media_type: str, media_count: int, media_payloads: list) -> PlazaPostOut:
    user = await get_current_user(session)
    body = content.strip()
    if not body:
        raise HTTPException(status_code=422, detail="EMPTY_PLAZA_CONTENT")
    post_id = new_id("plaza")
    count = len(media_payloads) if media_payloads else media_count
    if media_type == "text":
        count = 0
    normalized_media_type = media_type if count > 0 else "text"
    row = PlazaPost(id=post_id, author_id=user.id, author_name=user.nickname, icon_text=user.avatar_text or "海", topic="今日动态", content=body, media_type=normalized_media_type, media_count=count, gender=user.gender, verified=user.face_verified and user.gender_verified, city=user.city, age_range=user.age_range, view_count=0, like_count=0, comment_count=0, comment_preview=None, status="approved", distance_text="刚刚", created_at=now())
    session.add(row)
    if normalized_media_type != "text" and count > 0:
        for index in range(count):
            payload = media_payloads[index] if index < len(media_payloads) else None
            session.add(PlazaMedia(id=new_id("plaza_media"), post_id=post_id, owner_id=user.id, media_type=normalized_media_type, url=getattr(payload, "url", None) or default_media_url(normalized_media_type, post_id, index), storage_key=getattr(payload, "storage_key", None) or f"plaza/{post_id}_{index + 1}", mime_type=getattr(payload, "mime_type", None) or default_mime(normalized_media_type), size_bytes=getattr(payload, "size_bytes", None) or 0, duration_seconds=getattr(payload, "duration_seconds", None), width=getattr(payload, "width", None), height=getattr(payload, "height", None), status="approved", created_at=now()))
    await session.commit()
    return await to_plaza(session, row)


async def add_plaza_comment(session: AsyncSession, post_id: str, author_id: str, content: str, hidden: bool) -> PlazaPost | None:
    post = await session.get(PlazaPost, post_id)
    author = await session.get(User, author_id)
    if post is None or author is None:
        return None
    comment = PlazaComment(id=new_id("plaza_comment"), post_id=post_id, author_id=author.id, author_name=author.nickname, icon_text=author.avatar_text or "匿", author_gender=author.gender, author_age_range=author.age_range, author_verified=author.face_verified and author.gender_verified, author_city=author.city, content=content.strip(), hidden_for_owner_only=hidden, status="approved", created_at=now())
    session.add(comment)
    post.comment_count += 1
    if not hidden:
        post.comment_preview = content.strip()
    return post


async def comment_plaza(session: AsyncSession, post_id: str, content: str, hidden: bool) -> PlazaPostOut:
    await get_current_user(session)
    post = await add_plaza_comment(session, post_id, current_user_id(), content, hidden)
    if post is None:
        raise HTTPException(status_code=404, detail="PLAZA_POST_NOT_FOUND")
    await session.commit()
    return await to_plaza(session, post)


async def list_plaza_comments(session: AsyncSession, post_id: str, viewer_id: str | None = None) -> list[PlazaCommentOut]:
    await get_current_user(session)
    post = await session.get(PlazaPost, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="PLAZA_POST_NOT_FOUND")
    viewer = viewer_id or current_user_id()
    rows = (await session.execute(select(PlazaComment).where(PlazaComment.post_id == post_id, PlazaComment.status == "approved").order_by(PlazaComment.created_at))).scalars().all()
    result = []
    for row in rows:
        if row.hidden_for_owner_only and viewer != post.author_id:
            continue
        anonymize = row.hidden_for_owner_only
        author = None if anonymize else await session.get(User, row.author_id)
        result.append(PlazaCommentOut(id=row.id, post_id=row.post_id, author_id="anonymous" if anonymize else row.author_id, author_name="匿名留言" if anonymize else author.nickname if author else row.author_name, icon_text="匿" if anonymize else (author.avatar_text or "匿") if author else row.icon_text, icon_url=None if anonymize else author.avatar_url if author else None, author_gender="unknown" if anonymize else author.gender if author else row.author_gender, author_age_range=None if anonymize else author.age_range if author else row.author_age_range, author_verified=False if anonymize else (author.face_verified and author.gender_verified) if author else row.author_verified, author_city=None if anonymize else author.city if author else row.author_city, content=row.content, hidden_for_owner_only=row.hidden_for_owner_only, visible_to_owner_only=row.hidden_for_owner_only, created_at=iso(row.created_at)))
    return result


async def like_plaza(session: AsyncSession, post_id: str) -> PlazaPostOut:
    await get_current_user(session)
    post = await session.get(PlazaPost, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="PLAZA_POST_NOT_FOUND")
    existing = await session.scalar(select(PlazaLike).where(PlazaLike.post_id == post_id, PlazaLike.user_id == current_user_id()))
    if existing:
        await session.delete(existing)
        post.like_count = max(post.like_count - 1, 0)
    else:
        session.add(PlazaLike(id=new_id("plaza_like"), post_id=post_id, user_id=current_user_id(), created_at=now()))
        post.like_count += 1
    await session.commit()
    return await to_plaza(session, post)


async def wallet_state(session: AsyncSession) -> WalletState:
    await get_current_user(session)
    wallet = await session.get(WalletAccount, current_user_id())
    return WalletState(recharge_coins=wallet.recharge_coins, earned_coins=wallet.earned_coins, gift_coins=wallet.gift_coins, withdrawable_coins=wallet.withdrawable_coins, frozen_coins=wallet.frozen_coins, charm_value=wallet.charm_value, withdraw_threshold_charm=wallet.withdraw_threshold_charm, charm_exchange_rate=wallet.charm_exchange_rate)


async def wallet_overview(session: AsyncSession) -> tuple[WalletState, list[CoinLedgerItem], list[GiftProductOut]]:
    wallet = await wallet_state(session)
    ledger_rows = (await session.execute(select(CoinLedger).where(CoinLedger.user_id == current_user_id()).order_by(desc(CoinLedger.created_at)))).scalars().all()
    gift_rows = (await session.execute(select(GiftProduct).where(GiftProduct.status == "active").order_by(GiftProduct.sort_order))).scalars().all()
    return (
        wallet,
        [CoinLedgerItem(id=row.id, title=row.title, amount=row.amount, coin_bucket=row.coin_bucket, withdrawable=row.withdrawable, created_at=iso(row.created_at)) for row in ledger_rows],
        [GiftProductOut(id=row.id, name=row.name, price_coins=row.price_coins, icon_text=row.icon_text) for row in gift_rows],
    )


async def recharge_wallet(session: AsyncSession, amount: int, channel: str = "mock") -> tuple[str, WalletState]:
    await get_current_user(session)
    wallet = await session.get(WalletAccount, current_user_id())
    wallet.recharge_coins += amount
    wallet.updated_at = now()
    order = PaymentOrder(id=new_id("pay"), user_id=current_user_id(), channel=channel, amount_coins=amount, amount_cents=amount * 100, status="paid", prepay_id=new_id("prepay"), transaction_id=new_id("txn"), created_at=now(), paid_at=now())
    session.add(order)
    session.add(CoinLedger(id=new_id("ledger"), user_id=current_user_id(), title=f"充值金币 {amount}", amount=amount, coin_bucket="recharge", withdrawable=False, business_type="recharge", business_id=order.id, created_at=now()))
    await add_notification(session, "充值成功", f"金币 +{amount} 已到账。", "payment", order.id)
    await session.commit()
    return order.id, await wallet_state(session)


async def send_gift(session: AsyncSession, gift_id: str, receiver_id: str, source_type: str = "plaza", source_id: str | None = None) -> WalletState:
    await get_current_user(session)
    gift = await session.get(GiftProduct, gift_id)
    receiver = await session.get(User, receiver_id)
    wallet = await session.get(WalletAccount, current_user_id())
    if gift is None:
        raise HTTPException(status_code=404, detail="GIFT_NOT_FOUND")
    if receiver is None:
        raise HTTPException(status_code=404, detail="RECEIVER_NOT_FOUND")
    if wallet.recharge_coins < gift.price_coins:
        raise HTTPException(status_code=409, detail="COIN_NOT_ENOUGH")
    wallet.recharge_coins -= gift.price_coins
    wallet.gift_coins += gift.price_coins
    wallet.updated_at = now()
    session.add(GiftOrder(id=new_id("gift_order"), gift_id=gift.id, sender_id=current_user_id(), receiver_id=receiver_id, source_type=source_type, source_id=source_id, price_coins=gift.price_coins, status="sent", created_at=now()))
    session.add(CoinLedger(id=new_id("ledger"), user_id=current_user_id(), title=f"送出礼物：{gift.name}", amount=-gift.price_coins, coin_bucket="recharge", withdrawable=False, business_type="gift", business_id=gift.id, created_at=now()))
    await add_notification(session, "礼物已送出", f"你送出了 {gift.name}。", "gift", gift.id)
    await session.commit()
    return await wallet_state(session)


async def list_creators(session: AsyncSession) -> list[CreatorProfile]:
    await get_current_user(session)
    rows = (await session.execute(select(User).where(User.role == "creator", User.status == "active"))).scalars().all()
    return [CreatorProfile(user_id=row.id, display_name=row.nickname, gender=row.gender if row.gender in {"female", "male", "unknown"} else "unknown", verified=row.face_verified, safety_score=96 if row.face_verified else 82, follower_count=1280 if row.id == CREATOR_IDS["creator_001"] else 420, album_count=2, earned_coins=180, charm_value=row.charm_value) for row in rows]


async def list_private_photos(session: AsyncSession) -> list[PrivatePhoto]:
    await get_current_user(session)
    rows = (await session.execute(select(PrivatePhotoAsset).where(PrivatePhotoAsset.status == "approved"))).scalars().all()
    return [PrivatePhoto(id=row.id, owner_id=row.owner_id, owner_name=row.owner_name, title=row.title, cover_tone=row.cover_tone, price_coins=row.price_coins, blurred=current_user_id() not in row.purchased_by_user_ids.split(","), status=row.status, purchased=current_user_id() in row.purchased_by_user_ids.split(",")) for row in rows]


async def unlock_private_photo(session: AsyncSession, photo_id: str) -> PhotoUnlockResponse:
    await get_current_user(session)
    photo = await session.get(PrivatePhotoAsset, photo_id)
    wallet = await session.get(WalletAccount, current_user_id())
    if photo is None:
        raise HTTPException(status_code=404, detail="PHOTO_NOT_FOUND")
    purchased = set(filter(None, photo.purchased_by_user_ids.split(",")))
    if current_user_id() not in purchased:
        if wallet.recharge_coins < photo.price_coins:
            raise HTTPException(status_code=409, detail="COIN_NOT_ENOUGH")
        wallet.recharge_coins -= photo.price_coins
        purchased.add(current_user_id())
        photo.purchased_by_user_ids = ",".join(sorted(purchased))
        session.add(CoinLedger(id=new_id("ledger"), user_id=current_user_id(), title=f"解锁私密照片：{photo.title}", amount=-photo.price_coins, coin_bucket="recharge", withdrawable=False, business_type="private_photo", business_id=photo.id, created_at=now()))
        await session.commit()
    photo_out = PrivatePhoto(id=photo.id, owner_id=photo.owner_id, owner_name=photo.owner_name, title=photo.title, cover_tone=photo.cover_tone, price_coins=photo.price_coins, blurred=False, status=photo.status, purchased=True)
    return PhotoUnlockResponse(photo=photo_out, wallet=await wallet_state(session))


async def verification_overview(session: AsyncSession) -> tuple[VerificationState, ReferralState]:
    await get_current_user(session)
    v = await session.get(VerificationProfile, current_user_id())
    r = await session.get(ReferralAccount, current_user_id())
    return (
        VerificationState(face_verified=v.face_verified, gender_verified=v.gender_verified, detected_gender=v.detected_gender, liveness_passed=v.liveness_passed, manual_review_status=v.manual_review_status),
        ReferralState(invite_code=r.invite_code, invited_count=r.invited_count, reward_vip_days=r.reward_vip_days, next_reward_need=r.next_reward_need),
    )


async def submit_verification(session: AsyncSession) -> VerificationState:
    await get_current_user(session)
    v = await session.get(VerificationProfile, current_user_id())
    if v is None:
        v = VerificationProfile(user_id=current_user_id(), manual_review_status="not_submitted")
        session.add(v)
    if v.manual_review_status == "approved":
        return VerificationState(face_verified=v.face_verified, gender_verified=v.gender_verified, detected_gender=v.detected_gender, liveness_passed=v.liveness_passed, manual_review_status=v.manual_review_status)
    v.face_verified = True
    v.gender_verified = True
    v.liveness_passed = True
    v.detected_gender = "female"
    v.manual_review_status = "pending"
    v.submitted_at = now()
    v.reviewed_at = None
    user = await session.get(User, current_user_id())
    user.face_verified = False
    user.gender_verified = False
    await add_notification(session, "实名验证已提交", "资料已进入人工复核，通过后会点亮已认证标记。", "verification", current_user_id())
    await session.commit()
    return (await verification_overview(session))[0]


async def review_verification(session: AsyncSession, user_id: str, action: str, reason: str | None = None) -> VerificationState:
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="USER_NOT_FOUND")
    v = await session.get(VerificationProfile, user_id)
    if v is None:
        v = VerificationProfile(user_id=user_id, manual_review_status="not_submitted")
        session.add(v)
    approved = action == "approve"
    v.face_verified = approved
    v.gender_verified = approved
    v.liveness_passed = approved or v.liveness_passed
    v.detected_gender = user.gender if user.gender in {"female", "male"} else v.detected_gender
    v.manual_review_status = "approved" if approved else "rejected"
    v.reviewed_at = now()
    user.face_verified = approved
    user.gender_verified = approved
    session.add(AdminAuditLog(id=new_id("audit"), actor="admin", action=f"verification_{action}", target_type="verification", target_id=user_id, detail=reason, created_at=now()))
    await session.commit()
    return VerificationState(face_verified=v.face_verified, gender_verified=v.gender_verified, detected_gender=v.detected_gender, liveness_passed=v.liveness_passed, manual_review_status=v.manual_review_status)


async def list_blacklist(session: AsyncSession) -> list[BlacklistItem]:
    await get_current_user(session)
    rows = (await session.execute(select(BlacklistEntry).where(BlacklistEntry.owner_id == current_user_id(), BlacklistEntry.status == "blocked").order_by(desc(BlacklistEntry.blocked_at)))).scalars().all()
    return [BlacklistItem(id=row.id, user_id=row.blocked_user_id, nickname=row.nickname, reason=row.reason, blocked_at=iso(row.blocked_at)) for row in rows]


async def list_nearby(session: AsyncSession, city: str | None = None, gender: str | None = None, age_range: str | None = None, distance_km: float | None = None) -> list[NearbyUser]:
    await get_current_user(session)
    rows = (await session.execute(select(User).where(User.role == "creator", User.status == "active"))).scalars().all()
    normalized = normalize_gender(gender)
    if city and city not in {"全国", "all", "全部"}:
        rows = [row for row in rows if row.city == city]
    if normalized:
        rows = [row for row in rows if row.gender == normalized]
    if age_range and age_range not in {"全部", "all"}:
        rows = [row for row in rows if age_ranges_overlap(row.age_range, age_range)]
    result = []
    for index, row in enumerate(rows, start=1):
        distance = 1.2 + index
        if distance_km is not None and distance > distance_km:
            continue
        result.append(NearbyUser(id=row.id, nickname=row.nickname, icon_text=row.avatar_text or row.nickname[:1], icon_url=resolved_avatar_url(row, row.id), gender=row.gender, verified=row.face_verified, age_range=row.age_range, city=row.city, distance_km=distance, distance_text=f"{distance:.1f}km", signature="只接受礼貌的关注和好友申请。", is_vip=row.is_vip, online=index % 2 == 1))
    return result


async def create_game_random_match(session: AsyncSession, payload: GameRandomMatchRequest) -> GameRandomMatchResponse:
    user = await get_current_user(session)
    age_range = payload.age_range if payload.age_range not in {None, "", "全部", "all"} else None
    candidates = await list_nearby(session, gender=payload.gender, age_range=age_range)
    candidates = [candidate for candidate in candidates if candidate.id != user.id]
    if not candidates:
        raise HTTPException(status_code=404, detail="GAME_MATCH_NOT_FOUND")

    seed = int(hashlib.sha1(f"{user.id}:{payload.client_match_id}".encode("utf-8")).hexdigest()[:8], 16)
    target = candidates[seed % len(candidates)]
    quota_type = QuotaType.truth if payload.mode == "truth" else QuotaType.dare
    quota = await consume_quota(session, quota_type, f"game_random_match:{payload.client_match_id}")

    room = GameRoom(id=new_id("room"), owner_id=user.id, thread_id=None, mode=payload.mode, status="matched", created_at=now())
    session.add(room)
    await add_notification(
        session,
        "随机匹配已就绪",
        "已为你匹配到游戏对象；进入房间后仍需明确互动或确认，才可开启上下文私聊。",
        "game_match",
        room.id,
    )
    await session.commit()
    return GameRandomMatchResponse(
        match_id=f"match_{payload.client_match_id}",
        room_id=room.id,
        mode=payload.mode,
        status="matched",
        target_user=target,
        quota=quota,
        source_type="game_room",
        source_id=room.id,
        evidence_id=f"game_random_match:{room.id}",
        next_action="wait_confirm",
    )


async def follow_user(session: AsyncSession, target_user_id: str) -> dict[str, str]:
    await get_current_user(session)
    target = await session.get(User, target_user_id)
    if target is None:
        raise HTTPException(status_code=404, detail="USER_NOT_FOUND")
    exists = await session.scalar(select(Follow).where(Follow.follower_id == current_user_id(), Follow.target_user_id == target_user_id))
    if exists is None:
        session.add(Follow(id=new_id("follow"), follower_id=current_user_id(), target_user_id=target_user_id, created_at=now()))
        await add_notification(session, "关注成功", "对方动态会优先出现在你的推荐流里。", "follow", target_user_id)
        await session.commit()
    return {"status": "followed", "target_user_id": target_user_id}


async def request_friend(session: AsyncSession, target_user_id: str) -> dict[str, str]:
    await get_current_user(session)
    target = await session.get(User, target_user_id)
    if target is None:
        raise HTTPException(status_code=404, detail="USER_NOT_FOUND")
    exists = await session.scalar(select(FriendRequest).where(FriendRequest.requester_id == current_user_id(), FriendRequest.target_user_id == target_user_id))
    if exists is None:
        session.add(FriendRequest(id=new_id("friend"), requester_id=current_user_id(), target_user_id=target_user_id, status="requested", created_at=now()))
        await add_notification(session, "好友申请已发送", "好友用于长期关系沉淀；明确互动上下文内仍可按规则继续聊。", "friend", target_user_id)
        await session.commit()
    return {"status": "requested", "target_user_id": target_user_id}


async def create_match_expand_context_request(session: AsyncSession, target_user_id: str) -> MatchExpandContextResponse:
    from app import chat_store

    user = await get_current_user(session)
    target = await session.get(User, target_user_id)
    if target is None:
        raise HTTPException(status_code=404, detail="USER_NOT_FOUND")
    if target_user_id == user.id:
        raise HTTPException(status_code=422, detail={"code": "CHAT_TARGET_INVALID", "message": "Cannot start a context chat with yourself"})

    source_id = f"nearby:{target_user_id}"
    gate = "vip" if user.is_vip else "drift_coins"
    existing_request = await session.scalar(
        select(ChatContextRequestRecord)
        .where(
            ChatContextRequestRecord.initiator_id == user.id,
            ChatContextRequestRecord.target_user_id == target_user_id,
            ChatContextRequestRecord.source_type == "match_expand",
            ChatContextRequestRecord.source_id == source_id,
            ChatContextRequestRecord.status.in_(["pending", "active"]),
        )
        .order_by(desc(ChatContextRequestRecord.created_at))
    )
    existing_thread = None
    if existing_request is not None and existing_request.conversation_id:
        existing_thread = await session.get(ConversationThread, existing_request.conversation_id)
    if existing_request is not None and existing_thread is not None:
        return MatchExpandContextResponse(
            request=chat_store.to_request_out(existing_request),
            gate=gate,
            cost_coins=0,
            remaining_drift_coins=user.drift_coins,
            user=to_user_profile(user),
            thread_id=existing_thread.id,
        )

    cost = 0 if user.is_vip or existing_request is not None else MATCH_EXPAND_CHAT_COST
    if cost and user.drift_coins < cost:
        raise HTTPException(status_code=409, detail={"code": "MATCH_EXPAND_COIN_NOT_ENOUGH", "message": "需要 VIP 或至少 5 积分才能开聊。"})

    if cost:
        user.drift_coins -= cost
    thread = await _create_nearby_direct_thread(session, user, target)
    if existing_request is None:
        existing_request = ChatContextRequestRecord(
            id=new_id("ctx"),
            initiator_id=user.id,
            target_user_id=target_user_id,
            source_type="match_expand",
            source_id=source_id,
            source_title="附近的人直接开聊",
            reply_id=f"nearby:{user.id}:{target_user_id}",
            initiator_action="direct_chat",
            evidence_id=f"nearby_gate:{gate}",
            status="active",
            conversation_id=thread.id,
            confirm_action="direct_chat",
            confirm_evidence_id=f"nearby_direct:{thread.id}",
            audit_refs="[]",
            created_at=now(),
            updated_at=now(),
        )
        session.add(existing_request)
    else:
        existing_request.status = "active"
        existing_request.conversation_id = thread.id
        existing_request.confirm_action = "direct_chat"
        existing_request.confirm_evidence_id = f"nearby_direct:{thread.id}"
        existing_request.updated_at = now()
    await add_notification(
        session,
        "附近的人已开聊",
        f"已与 {target.nickname} 开启聊天；本次来源、频控、举报和拉黑证据已保留。",
        "match_expand",
        thread.id,
    )
    await session.commit()
    await session.refresh(user)
    await session.refresh(existing_request)
    return MatchExpandContextResponse(
        request=chat_store.to_request_out(existing_request),
        gate=gate,
        cost_coins=cost,
        remaining_drift_coins=user.drift_coins,
        user=to_user_profile(user),
        thread_id=thread.id,
    )


async def _create_nearby_direct_thread(session: AsyncSession, user: User, target: User) -> ConversationThread:
    existing_thread = await session.scalar(
        select(ConversationThread)
        .where(
            ConversationThread.user_a_id == user.id,
            ConversationThread.user_b_id == target.id,
            ConversationThread.participant_tag == "附近开聊",
            ConversationThread.status.in_(["active", "risk_frozen"]),
        )
        .order_by(desc(ConversationThread.updated_at))
    )
    if existing_thread is not None:
        return existing_thread

    thread = ConversationThread(
        id=new_id("thread"),
        bottle_id=None,
        user_a_id=user.id,
        user_b_id=target.id,
        participant_name=target.nickname,
        participant_tag="附近开聊",
        bottle_preview=f"附近的人 · {target.city or '同城'} · {target.age_range or '年龄未知'}",
        last_message="已通过附近的人开聊。",
        unread_count=0,
        status="active",
        created_at=now(),
        updated_at=now(),
    )
    session.add(thread)
    session.add(
        ConversationTurn(
            id=new_id("turn"),
            thread_id=thread.id,
            sender_id=user.id,
            sender_name=user.nickname,
            body="已通过附近的人开聊。",
            turn_type="text",
            created_at=now(),
        )
    )
    return thread


async def create_report(session: AsyncSession, target_type: str, target_id: str, reason: str) -> ReportOut:
    await get_current_user(session)
    existing = await session.scalar(select(ContentReport).where(ContentReport.reporter_id == current_user_id(), ContentReport.target_type == target_type, ContentReport.target_id == target_id, ContentReport.reason == reason))
    if existing is None:
        existing = ContentReport(id=new_id("report"), reporter_id=current_user_id(), target_type=target_type, target_id=target_id, reason=reason, status="queued", created_at=now())
        session.add(existing)
        await add_notification(session, "举报已提交", "内容已进入审核队列，审核员会结合上下文处理。", "report", existing.id)
        await session.commit()
    return ReportOut(id=existing.id, reporter_id=existing.reporter_id, target_type=existing.target_type, target_id=existing.target_id, reason=existing.reason, status=existing.status, created_at=iso(existing.created_at), evidence_refs=[f"{existing.target_type}:{existing.target_id}"])


async def list_reports(session: AsyncSession, status_filter: str | None = None, target_type_filter: str | None = None, q: str | None = None) -> list[ReportOut]:
    await get_current_user(session)
    query = select(ContentReport)
    if status_filter and status_filter != "all":
        query = query.where(ContentReport.status == status_filter)
    if target_type_filter and target_type_filter != "all":
        query = query.where(ContentReport.target_type == target_type_filter)
    rows = (await session.execute(query.order_by(desc(ContentReport.created_at)))).scalars().all()
    if not rows:
        return []

    target_type_labels = {
        "user": "用户",
        "bottle": "漂流瓶",
        "treehole": "树洞",
        "reply": "回应",
        "chat": "私信聊天",
        "plaza": "广场",
        "private_photo": "私密照片",
    }

    user_target_ids = [row.target_id for row in rows if row.target_type == "user"]
    bottle_target_ids = [row.target_id for row in rows if row.target_type == "bottle"]
    treehole_target_ids = [row.target_id for row in rows if row.target_type == "treehole"]
    reply_target_ids = [row.target_id for row in rows if row.target_type == "reply"]
    plaza_target_ids = [row.target_id for row in rows if row.target_type == "plaza"]
    private_photo_target_ids = [row.target_id for row in rows if row.target_type == "private_photo"]
    chat_target_ids = [row.target_id for row in rows if row.target_type == "chat"]

    users = await _user_map(
        session,
        list({
            *user_target_ids,
            *([row.author_id for row in (await session.execute(select(Bottle).where(Bottle.id.in_(bottle_target_ids)))).scalars().all()] if bottle_target_ids else []),
            *([row.author_id for row in (await session.execute(select(TreeholePost).where(TreeholePost.id.in_(treehole_target_ids)))).scalars().all()] if treehole_target_ids else []),
            *([row.author_id for row in (await session.execute(select(BottleReply).where(BottleReply.id.in_(reply_target_ids)))).scalars().all()] if reply_target_ids else []),
            *([row.author_id for row in (await session.execute(select(PlazaComment).where(PlazaComment.id.in_(reply_target_ids)))).scalars().all()] if reply_target_ids else []),
            *([row.author_id for row in (await session.execute(select(PlazaPost).where(PlazaPost.id.in_(plaza_target_ids)))).scalars().all()] if plaza_target_ids else []),
            *([row.owner_id for row in (await session.execute(select(PrivatePhotoAsset).where(PrivatePhotoAsset.id.in_(private_photo_target_ids)))).scalars().all()] if private_photo_target_ids else []),
        })
    )

    bottle_rows = {
        row.id: row
        for row in (
            await session.execute(select(Bottle).where(Bottle.id.in_(bottle_target_ids)))
        ).scalars().all()
    } if bottle_target_ids else {}
    plaza_comment_rows = {
        row.id: row
        for row in (
            await session.execute(select(PlazaComment).where(PlazaComment.id.in_(reply_target_ids)))
        ).scalars().all()
    } if reply_target_ids else {}
    treehole_rows = {
        row.id: row
        for row in (
            await session.execute(select(TreeholePost).where(TreeholePost.id.in_(treehole_target_ids)))
        ).scalars().all()
    } if treehole_target_ids else {}
    reply_rows = {
        row.id: row
        for row in (
            await session.execute(select(BottleReply).where(BottleReply.id.in_(reply_target_ids)))
        ).scalars().all()
    } if reply_target_ids else {}
    plaza_rows = {
        row.id: row
        for row in (
            await session.execute(select(PlazaPost).where(PlazaPost.id.in_(plaza_target_ids)))
        ).scalars().all()
    } if plaza_target_ids else {}
    private_photo_rows = {
        row.id: row
        for row in (
            await session.execute(select(PrivatePhotoAsset).where(PrivatePhotoAsset.id.in_(private_photo_target_ids)))
        ).scalars().all()
    } if private_photo_target_ids else {}
    chat_rows = {
        row.id: row
        for row in (
            await session.execute(select(ConversationThread).where(ConversationThread.id.in_(chat_target_ids)))
        ).scalars().all()
    } if chat_target_ids else {}
    audit_rows = {
        row.target_id: row.id
        for row in (
            await session.execute(select(AdminAuditLog).where(AdminAuditLog.target_id.in_([report.id for report in rows])))
        ).scalars().all()
    }

    result: list[ReportOut] = []
    for row in rows:
        display_name: str | None = None
        avatar_text: str | None = None
        avatar_url: str | None = None
        target_preview: str | None = row.reason
        evidence_refs = [f"report:{row.id}", f"{row.target_type}:{row.target_id}", f"reporter:{row.reporter_id}"]

        if row.target_type == "user":
            target_user = users.get(row.target_id)
            if target_user:
                display_name = target_user.nickname
                avatar_text = target_user.avatar_text
                avatar_url = target_user.avatar_url
                target_preview = f"UID: {row.target_id[-8:]}"
        elif row.target_type == "bottle" and row.target_id in bottle_rows:
            content = bottle_rows[row.target_id]
            target_owner = users.get(content.author_id)
            display_name = f"{target_owner.nickname if target_owner else content.author_name} 的漂流瓶"
            avatar_text = content.author_avatar_text
            avatar_url = target_owner.avatar_url if target_owner else None
            target_preview = content.content[:60]
            evidence_refs.append(f"content_status:{content.status}")
        elif row.target_type == "treehole" and row.target_id in treehole_rows:
            content = treehole_rows[row.target_id]
            target_owner = users.get(content.author_id)
            display_name = f"{target_owner.nickname if target_owner else content.author_name} 的树洞"
            avatar_text = content.author_avatar_text
            avatar_url = content.author_avatar_url
            target_preview = content.content[:60]
        elif row.target_type == "reply" and row.target_id in reply_rows:
            reply = reply_rows[row.target_id]
            target_owner = users.get(reply.author_id)
            display_name = f"{target_owner.nickname if target_owner else reply.id} 的留言"
            target_preview = reply.content[:60]
            avatar_text = target_owner.avatar_text if target_owner else None
            avatar_url = target_owner.avatar_url if target_owner else None
            evidence_refs.extend([f"content_type:bottle_reply", f"content_status:{reply.status}"])
        elif row.target_type == "reply" and row.target_id in plaza_comment_rows:
            comment = plaza_comment_rows[row.target_id]
            target_owner = users.get(comment.author_id)
            display_name = f"{target_owner.nickname if target_owner else comment.author_name} 的广场留言"
            target_preview = comment.content[:60]
            avatar_text = target_owner.avatar_text if target_owner else None
            avatar_url = target_owner.avatar_url if target_owner else None
            evidence_refs.extend([f"content_type:plaza_comment", f"content_status:{comment.status}", f"plaza:{comment.post_id}"])
        elif row.target_type == "plaza" and row.target_id in plaza_rows:
            content = plaza_rows[row.target_id]
            target_owner = users.get(content.author_id)
            display_name = f"{target_owner.nickname if target_owner else content.author_name} 的广场内容"
            avatar_text = target_owner.avatar_text if target_owner else None
            avatar_url = target_owner.avatar_url if target_owner else None
            target_preview = (content.content[:60] if content.content else "")
            evidence_refs.append(f"content_status:{content.status}")
        elif row.target_type == "private_photo" and row.target_id in private_photo_rows:
            private_photo = private_photo_rows[row.target_id]
            target_owner = users.get(private_photo.owner_id)
            display_name = f"{target_owner.nickname if target_owner else private_photo.owner_name} 的私密照"
            avatar_text = target_owner.avatar_text if target_owner else None
            avatar_url = target_owner.avatar_url if target_owner else None
            target_preview = private_photo.title
            if private_photo.audit_refs:
                evidence_refs.extend([ref for ref in private_photo.audit_refs.split(",") if ref])
        elif row.target_type == "chat" and row.target_id in chat_rows:
            thread = chat_rows[row.target_id]
            display_name = thread.participant_name or "匿名对话"
            target_preview = thread.bottle_preview or thread.last_message or ""
            participant_user = users.get(thread.user_a_id)
            avatar_text = participant_user.avatar_text if participant_user else None
            avatar_url = participant_user.avatar_url if participant_user else None
            evidence_refs.extend([f"conversation:{thread.id}", f"thread_status:{thread.status}"])
            if thread.bottle_id:
                evidence_refs.append(f"bottle:{thread.bottle_id}")

        audit_refs = [audit_rows[row.id]] if row.id in audit_rows else []
        item = ReportOut(
            id=row.id,
            reporter_id=row.reporter_id,
            target_type=row.target_type,
            target_id=row.target_id,
            reason=row.reason,
            status=row.status,
            created_at=iso(row.created_at),
            target_type_text=target_type_labels.get(row.target_type),
            target_display_name=display_name,
            target_avatar_text=avatar_text,
            target_avatar_url=avatar_url,
            target_preview=target_preview,
            evidence_refs=list(dict.fromkeys(evidence_refs)),
            audit_refs=audit_refs,
        )
        keyword = (q or "").strip().lower()
        searchable = " ".join(
            [
                item.id,
                item.reporter_id or "",
                item.target_type,
                item.target_id,
                item.reason,
                item.target_type_text or "",
                item.target_display_name or "",
                item.target_preview or "",
                " ".join(item.evidence_refs),
                " ".join(item.audit_refs),
            ]
        ).lower()
        if keyword and keyword not in searchable:
            continue
        result.append(item)
    return result


async def resolve_report(
    session: AsyncSession,
    report_id: str,
    reason: str,
    actor: str,
    penalty_action: str = "none",
) -> dict[str, str | None]:
    report = await session.get(ContentReport, report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="REPORT_NOT_FOUND")

    before_status = report.status
    report.status = "resolved"
    penalty_target_user_id: str | None = None
    penalty_target_thread_id: str | None = None
    penalty_target_content_id: str | None = None
    penalty_target_content_type: str | None = None
    penalty_audit_id: str | None = None
    if penalty_action in {"limit_user", "freeze_chat"}:
        if report.target_type != "chat":
            raise HTTPException(status_code=422, detail="REPORT_PENALTY_UNSUPPORTED")
        thread = await session.get(ConversationThread, report.target_id)
        if thread is None:
            raise HTTPException(status_code=404, detail="REPORT_TARGET_NOT_FOUND")
    if penalty_action == "limit_user":
        penalty_target_user_id = thread.user_b_id if report.reporter_id == thread.user_a_id else thread.user_a_id
        target_user = await session.get(User, penalty_target_user_id)
        if target_user is None:
            raise HTTPException(status_code=404, detail="REPORT_TARGET_USER_NOT_FOUND")
        target_user.status = "limited"
        restriction = (await _latest_restriction_map(session, [penalty_target_user_id])).get(penalty_target_user_id)
        if restriction:
            restriction.status = "limited"
            restriction.reason = reason
            restriction.blocked_until = None
            restriction.updated_at = now()
        else:
            session.add(
                AdminUserRestriction(
                    id=new_id("admin_restriction"),
                    user_id=penalty_target_user_id,
                    status="limited",
                    reason=reason,
                    blocked_until=None,
                    action_by=actor,
                    created_at=now(),
                    updated_at=now(),
                )
            )
        penalty_audit_id = new_id("audit")
        session.add(
            AdminAuditLog(
                id=penalty_audit_id,
                actor=actor,
                action="report_penalty_limit_user",
                target_type="user",
                target_id=penalty_target_user_id,
                detail=f"report={report.id};thread={report.target_id};reason={reason}",
                created_at=now(),
            )
        )
    elif penalty_action == "freeze_chat":
        penalty_target_thread_id = thread.id
        before_thread_status = thread.status
        thread.status = "risk_frozen"
        await add_user_notification(
            session,
            report.reporter_id,
            "聊天已被冻结",
            f"你举报的聊天已因风险处置被冻结。原因：{reason}。如需申诉或补充证据，请在客服入口提交说明。",
            "chat_freeze",
            thread.id,
        )
        penalty_audit_id = new_id("audit")
        session.add(
            AdminAuditLog(
                id=penalty_audit_id,
                actor=actor,
                action="report_penalty_freeze_chat",
                target_type="chat",
                target_id=thread.id,
                detail=f"report={report.id};before_status={before_thread_status};after_status=risk_frozen;reason={reason}",
                created_at=now(),
            )
        )
    elif penalty_action == "offline_content":
        content_owner_id: str | None = None
        content_before_status: str | None = None
        content_after_status = "rejected"
        if report.target_type == "bottle":
            content = await session.get(Bottle, report.target_id)
            penalty_target_content_type = "bottle"
            if content:
                content_owner_id = content.author_id
                content_before_status = content.status
                content.status = content_after_status
        elif report.target_type == "plaza":
            content = await session.get(PlazaPost, report.target_id)
            penalty_target_content_type = "plaza"
            if content:
                content_owner_id = content.author_id
                content_before_status = content.status
                content.status = content_after_status
        elif report.target_type == "reply":
            plaza_comment = await session.get(PlazaComment, report.target_id)
            if plaza_comment:
                penalty_target_content_type = "plaza_comment"
                content_owner_id = plaza_comment.author_id
                content_before_status = plaza_comment.status
                plaza_comment.status = content_after_status
                post = await session.get(PlazaPost, plaza_comment.post_id)
                if post and content_before_status == "approved":
                    post.comment_count = max(0, post.comment_count - 1)
                    if post.comment_preview == plaza_comment.content:
                        post.comment_preview = ""
            else:
                bottle_reply = await session.get(BottleReply, report.target_id)
                penalty_target_content_type = "bottle_reply"
                if bottle_reply:
                    content_owner_id = bottle_reply.author_id
                    content_before_status = bottle_reply.status
                    bottle_reply.status = content_after_status
        else:
            raise HTTPException(status_code=422, detail="REPORT_PENALTY_UNSUPPORTED")
        if content_before_status is None or penalty_target_content_type is None:
            raise HTTPException(status_code=404, detail="REPORT_TARGET_NOT_FOUND")
        penalty_target_content_id = report.target_id
        if content_owner_id:
            await add_user_notification(
                session,
                content_owner_id,
                "内容已下线",
                f"你被举报的内容已因审核处置下线。原因：{reason}。如需申诉，请在客服入口提交说明。",
                "content_offline",
                report.target_id,
            )
        penalty_audit_id = new_id("audit")
        session.add(
            AdminAuditLog(
                id=penalty_audit_id,
                actor=actor,
                action="report_penalty_offline_content",
                target_type=penalty_target_content_type,
                target_id=report.target_id,
                detail=f"report={report.id};before_status={content_before_status};after_status={content_after_status};reason={reason}",
                created_at=now(),
            )
        )
    elif penalty_action != "none":
        raise HTTPException(status_code=422, detail="REPORT_PENALTY_UNSUPPORTED")

    audit_id = new_id("audit")
    audit_detail = f"before={before_status};after=resolved;reason={reason};penalty_action={penalty_action}"
    if penalty_target_user_id:
        audit_detail = f"{audit_detail};penalty_target_user_id={penalty_target_user_id}"
    if penalty_target_thread_id:
        audit_detail = f"{audit_detail};penalty_target_thread_id={penalty_target_thread_id}"
    if penalty_target_content_id:
        audit_detail = f"{audit_detail};penalty_target_content_id={penalty_target_content_id};penalty_target_content_type={penalty_target_content_type}"
    session.add(
        AdminAuditLog(
            id=audit_id,
            actor=actor,
            action="report_resolve",
            target_type="report",
            target_id=report.id,
            detail=audit_detail,
            created_at=now(),
        )
    )
    await session.commit()
    return {
        "report_id": report.id,
        "before_status": before_status,
        "after_status": report.status,
        "reason": reason,
        "audit_id": audit_id,
        "resolved_at": iso(now()),
        "penalty_action": penalty_action,
        "penalty_target_user_id": penalty_target_user_id,
        "penalty_target_thread_id": penalty_target_thread_id,
        "penalty_target_content_id": penalty_target_content_id,
        "penalty_target_content_type": penalty_target_content_type,
        "penalty_audit_id": penalty_audit_id,
    }


async def restore_report_chat(
    session: AsyncSession,
    report_id: str,
    reason: str,
    actor: str,
) -> dict[str, str]:
    report = await session.get(ContentReport, report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="REPORT_NOT_FOUND")
    if report.target_type != "chat":
        raise HTTPException(status_code=422, detail="REPORT_PENALTY_UNSUPPORTED")
    thread = await session.get(ConversationThread, report.target_id)
    if thread is None:
        raise HTTPException(status_code=404, detail="REPORT_TARGET_NOT_FOUND")
    if thread.status != "risk_frozen":
        raise HTTPException(status_code=409, detail="REPORT_CHAT_NOT_FROZEN")

    before_thread_status = thread.status
    thread.status = "active"
    await add_user_notification(
        session,
        report.reporter_id,
        "聊天已恢复",
        f"你举报的聊天已由管理员恢复。原因：{reason}。",
        "chat_restore",
        thread.id,
    )
    audit_id = new_id("audit")
    session.add(
        AdminAuditLog(
            id=audit_id,
            actor=actor,
            action="report_restore_chat",
            target_type="chat",
            target_id=thread.id,
            detail=f"report={report.id};before_status={before_thread_status};after_status=active;reason={reason}",
            created_at=now(),
        )
    )
    await session.commit()
    return {
        "report_id": report.id,
        "thread_id": thread.id,
        "before_thread_status": before_thread_status,
        "after_thread_status": thread.status,
        "reason": reason,
        "audit_id": audit_id,
        "restored_at": iso(now()),
    }


def _parse_audit_refs(value: str | None) -> list[str]:
    if not value:
        return []
    try:
        refs = json.loads(value)
    except json.JSONDecodeError:
        return []
    return refs if isinstance(refs, list) else []


async def to_chat_appeal(session: AsyncSession, row: ChatAppeal) -> ChatAppealOut:
    user = await session.get(User, row.user_id)
    thread = await session.get(ConversationThread, row.thread_id)
    return ChatAppealOut(
        id=row.id,
        thread_id=row.thread_id,
        user_id=row.user_id,
        user_name=user.nickname if user else row.user_id,
        participant_name=thread.participant_name if thread else None,
        reason=row.reason,
        status=row.status,
        admin_reason=row.admin_reason,
        audit_refs=_parse_audit_refs(row.audit_refs),
        created_at=iso(row.created_at),
        updated_at=iso(row.updated_at),
    )


async def create_chat_appeal(session: AsyncSession, thread_id: str, reason: str) -> ChatAppealOut:
    user = await get_current_user(session)
    thread = await session.get(ConversationThread, thread_id)
    if thread is None or thread.user_a_id != user.id:
        raise HTTPException(status_code=404, detail="THREAD_NOT_FOUND")
    if thread.status != "risk_frozen":
        raise HTTPException(status_code=409, detail="CHAT_APPEAL_THREAD_NOT_FROZEN")

    existing = await session.scalar(
        select(ChatAppeal).where(
            ChatAppeal.thread_id == thread_id,
            ChatAppeal.user_id == user.id,
            ChatAppeal.status == "pending",
        )
    )
    if existing is not None:
        return await to_chat_appeal(session, existing)

    audit_id = new_id("audit")
    appeal = ChatAppeal(
        id=new_id("appeal"),
        thread_id=thread_id,
        user_id=user.id,
        reason=reason,
        status="pending",
        audit_refs=json.dumps([audit_id], ensure_ascii=False),
        created_at=now(),
        updated_at=now(),
    )
    session.add(appeal)
    session.add(
        AdminAuditLog(
            id=audit_id,
            actor=user.nickname,
            action="chat_appeal_submit",
            target_type="chat_appeal",
            target_id=appeal.id,
            detail=f"thread={thread_id};user={user.id};reason={reason}",
            created_at=now(),
        )
    )
    await add_user_notification(
        session,
        user.id,
        "申诉已提交",
        "你的冻结聊天申诉已进入后台处理，处理结果会通过系统消息通知。",
        "chat_appeal",
        appeal.id,
    )
    await session.commit()
    await session.refresh(appeal)
    return await to_chat_appeal(session, appeal)


async def list_chat_appeals(session: AsyncSession, status_filter: str | None = None) -> list[ChatAppealOut]:
    await get_current_user(session)
    query = select(ChatAppeal)
    if status_filter and status_filter != "all":
        query = query.where(ChatAppeal.status == status_filter)
    rows = (await session.execute(query.order_by(desc(ChatAppeal.updated_at)))).scalars().all()
    return [await to_chat_appeal(session, row) for row in rows]


async def review_chat_appeal(
    session: AsyncSession,
    appeal_id: str,
    action: str,
    reason: str,
    actor: str,
) -> dict[str, str]:
    appeal = await session.get(ChatAppeal, appeal_id)
    if appeal is None:
        raise HTTPException(status_code=404, detail="CHAT_APPEAL_NOT_FOUND")
    if appeal.status != "pending":
        raise HTTPException(status_code=409, detail="CHAT_APPEAL_ALREADY_REVIEWED")
    thread = await session.get(ConversationThread, appeal.thread_id)
    if thread is None:
        raise HTTPException(status_code=404, detail="THREAD_NOT_FOUND")

    before_status = appeal.status
    appeal.status = "approved" if action == "approve" else "rejected"
    appeal.admin_reason = reason
    appeal.updated_at = now()
    if action == "approve":
        thread.status = "active"
        thread.updated_at = now()
        notice_title = "申诉通过，聊天已恢复"
        notice_body = f"你的冻结聊天申诉已通过。处理原因：{reason}。"
        notice_type = "chat_appeal_approved"
    else:
        notice_title = "申诉未通过"
        notice_body = f"你的冻结聊天申诉未通过。处理原因：{reason}。"
        notice_type = "chat_appeal_rejected"

    audit_id = new_id("audit")
    refs = _parse_audit_refs(appeal.audit_refs)
    refs.append(audit_id)
    appeal.audit_refs = json.dumps(refs, ensure_ascii=False)
    session.add(
        AdminAuditLog(
            id=audit_id,
            actor=actor,
            action=f"chat_appeal_{action}",
            target_type="chat_appeal",
            target_id=appeal.id,
            detail=f"thread={thread.id};before={before_status};after={appeal.status};thread_status={thread.status};reason={reason}",
            created_at=now(),
        )
    )
    await add_user_notification(session, appeal.user_id, notice_title, notice_body, notice_type, thread.id)
    await session.commit()
    return {
        "appeal_id": appeal.id,
        "thread_id": thread.id,
        "before_status": before_status,
        "after_status": appeal.status,
        "thread_status": thread.status,
        "audit_id": audit_id,
        "reviewed_at": iso(now()),
    }


async def block_user(session: AsyncSession, blocked_user_id: str, reason: str = "用户拉黑") -> BlockOut:
    await get_current_user(session)
    target = await session.get(User, blocked_user_id)
    if target is None:
        target = User(id=blocked_user_id, nickname=blocked_user_id, role="user", avatar_text="黑", platform="h5", gender="unknown", is_vip=False, vip_level="none", drift_coins=0, face_verified=False, gender_verified=False, charm_value=0, status="active", created_at=now())
        session.add(target)
    existing = await session.scalar(select(BlacklistEntry).where(BlacklistEntry.owner_id == current_user_id(), BlacklistEntry.blocked_user_id == blocked_user_id))
    if existing is None:
        existing = BlacklistEntry(id=new_id("block"), owner_id=current_user_id(), blocked_user_id=blocked_user_id, nickname=target.nickname, reason=reason, status="blocked", blocked_at=now())
        session.add(existing)
        await add_notification(session, "已加入黑名单", f"{target.nickname}不会再出现在你的漂流瓶推荐里。", "block", blocked_user_id)
        await session.commit()
    return BlockOut(id=existing.id, blocked_user_id=existing.blocked_user_id, status="blocked", blocked_at=iso(existing.blocked_at))


async def list_blocks(session: AsyncSession) -> list[BlockOut]:
    rows = (await session.execute(select(BlacklistEntry).where(BlacklistEntry.owner_id == current_user_id()))).scalars().all()
    return [BlockOut(id=row.id, blocked_user_id=row.blocked_user_id, status="blocked", blocked_at=iso(row.blocked_at)) for row in rows]


async def list_messages(session: AsyncSession) -> list[MessageItemOut]:
    await get_current_user(session)
    rows = (await session.execute(select(MessageNotification).where(MessageNotification.user_id == current_user_id()).order_by(desc(MessageNotification.created_at)))).scalars().all()
    return [MessageItemOut(id=row.id, title=row.title, body=row.body, unread=row.unread, created_at=iso(row.created_at), business_type=row.business_type, business_id=row.business_id) for row in rows]


async def mark_messages_read(session: AsyncSession) -> dict[str, str]:
    await get_current_user(session)
    rows = (await session.execute(select(MessageNotification).where(MessageNotification.user_id == current_user_id(), MessageNotification.unread == True))).scalars().all()
    for row in rows:
        row.unread = False
    threads = (await session.execute(select(ConversationThread).where(ConversationThread.user_a_id == current_user_id()))).scalars().all()
    for thread in threads:
        thread.unread_count = 0
    await session.commit()
    return {"status": "ok"}


async def mark_message_read(session: AsyncSession, message_id: str) -> MessageItemOut:
    await get_current_user(session)
    row = await session.get(MessageNotification, message_id)
    if row is None or row.user_id != current_user_id():
        raise HTTPException(status_code=404, detail="MESSAGE_NOT_FOUND")
    row.unread = False
    await session.commit()
    await session.refresh(row)
    return MessageItemOut(
        id=row.id,
        title=row.title,
        body=row.body,
        unread=row.unread,
        created_at=iso(row.created_at),
        business_type=row.business_type,
        business_id=row.business_id,
    )


async def list_threads(session: AsyncSession) -> list[ConversationThreadOut]:
    await get_current_user(session)
    rows = (
        await session.execute(
            select(ConversationThread)
            .where(ConversationThread.user_a_id == current_user_id(), ConversationThread.status.in_(["active", "risk_frozen"]))
            .order_by(desc(ConversationThread.updated_at))
        )
    ).scalars().all()
    return [await to_thread(session, row) for row in rows]


async def mark_thread_read(session: AsyncSession, thread_id: str) -> ConversationThreadOut:
    await get_current_user(session)
    thread = await session.get(ConversationThread, thread_id)
    if thread is None or thread.user_a_id != current_user_id():
        raise HTTPException(status_code=404, detail="THREAD_NOT_FOUND")
    thread.unread_count = 0
    await session.commit()
    await session.refresh(thread)
    return await to_thread(session, thread)


async def to_thread(session: AsyncSession, row: ConversationThread) -> ConversationThreadOut:
    turn_rows = (await session.execute(select(ConversationTurn).where(ConversationTurn.thread_id == row.id).order_by(ConversationTurn.created_at))).scalars().all()
    participant = await session.get(User, row.user_b_id)
    frozen_notice = None
    if row.status == "risk_frozen":
        frozen_notice = "该聊天已因举报处置被冻结。若你认为处理有误，可在客服入口提交申诉说明。"
    return ConversationThreadOut(id=row.id, bottle_id=row.bottle_id, status=row.status, frozen_notice=frozen_notice, participant_user_id=row.user_b_id, participant_name=participant.nickname if participant else row.participant_name, participant_avatar_text=participant.avatar_text if participant else None, participant_avatar_url=resolved_avatar_url(participant, row.user_b_id), participant_tag=row.participant_tag, bottle_preview=row.bottle_preview, last_message=row.last_message, updated_at=iso(row.updated_at), unread_count=row.unread_count, turns=[await to_turn(session, turn) for turn in turn_rows])


async def to_turn(session: AsyncSession, row: ConversationTurn) -> ConversationTurnOut:
    gift = await session.get(GiftProduct, row.gift_id) if row.gift_id else None
    room = await session.get(GameRoom, row.game_room_id) if row.game_room_id else None
    from_me = row.sender_id == current_user_id()
    sender_name = row.sender_name
    if from_me:
        sender = await session.get(User, row.sender_id)
        sender_name = sender.nickname if sender else row.sender_name
    return ConversationTurnOut(id=row.id, sender_name=sender_name, body=row.body, created_at=iso(row.created_at), from_me=from_me, type=row.turn_type, media_url=row.media_url, media_duration=row.media_duration, flash_viewed=row.flash_viewed, gift_id=row.gift_id, gift_name=gift.name if gift else None, gift_icon_text=gift.icon_text if gift else None, gift_price_coins=gift.price_coins if gift else None, game_room_id=row.game_room_id, game_room_mode=room.mode if room else None)


def moderate_chat_body(body: str) -> tuple[str, list[str]]:
    masked = body.strip()
    matched: list[str] = []
    lowered = masked.lower()
    for word in CHAT_RISK_WORDS:
        if word.lower() in lowered:
            matched.append(word)
            masked = masked.replace(word, "*" * min(len(word), 8))
    return masked, matched


async def send_turn(session: AsyncSession, thread_id: str, body: str, turn_type: str = "text", media_url: str | None = None, media_duration: int | None = None) -> ConversationThreadOut:
    user = await get_current_user(session)
    thread = await session.get(ConversationThread, thread_id)
    if thread is None:
        raise HTTPException(status_code=404, detail="THREAD_NOT_FOUND")
    if thread.status == "risk_frozen":
        raise HTTPException(status_code=403, detail={"code": "CHAT_RISK_FROZEN", "message": "该聊天已因举报处置被冻结。"})
    if thread.status != "active":
        raise HTTPException(status_code=409, detail="THREAD_NOT_ACTIVE")
    clean_body, matched_words = moderate_chat_body(body)
    turn = ConversationTurn(id=new_id("turn"), thread_id=thread_id, sender_id=user.id, sender_name=user.nickname, body=clean_body, turn_type=turn_type, media_url=media_url, media_duration=media_duration, flash_viewed=False, created_at=now())
    session.add(turn)
    thread.last_message = clean_body
    thread.updated_at = now()
    thread.unread_count = 0
    if matched_words:
        reason = f"chat_risk:{','.join(matched_words[:5])}"
        report = await session.scalar(select(ContentReport).where(ContentReport.reporter_id == user.id, ContentReport.target_type == "chat", ContentReport.target_id == thread_id, ContentReport.reason == reason))
        if report is None:
            session.add(ContentReport(id=new_id("report"), reporter_id=user.id, target_type="chat", target_id=thread_id, reason=reason, status="reviewing", created_at=now()))
        await add_notification(session, "消息已进入审核", "聊天内容命中安全策略，已做脱敏并进入后台复核。", "chat", thread_id)
    await session.commit()
    return await to_thread(session, thread)


async def mark_turn_viewed(session: AsyncSession, thread_id: str, turn_id: str) -> ConversationThreadOut:
    await get_current_user(session)
    thread = await session.get(ConversationThread, thread_id)
    if thread is None:
        raise HTTPException(status_code=404, detail="THREAD_NOT_FOUND")
    turn = await session.get(ConversationTurn, turn_id)
    if turn is None or turn.thread_id != thread_id:
        raise HTTPException(status_code=404, detail="TURN_NOT_FOUND")
    if turn.turn_type not in {"flash_image", "flash_video"}:
        raise HTTPException(status_code=409, detail="NOT_FLASH_CONTENT")
    turn.flash_viewed = True
    await session.commit()
    return await to_thread(session, thread)


async def create_game_room(session: AsyncSession, thread_id: str, mode: str) -> tuple[str, ConversationThreadOut]:
    user = await get_current_user(session)
    thread = await session.get(ConversationThread, thread_id)
    if thread is None:
        raise HTTPException(status_code=404, detail="THREAD_NOT_FOUND")
    room = GameRoom(id=new_id("room"), owner_id=current_user_id(), thread_id=thread_id, mode=mode, status="open", created_at=now())
    session.add(room)
    mode_text = "真心话" if mode == "truth" else "大冒险" if mode == "dare" else "真心话大冒险"
    session.add(ConversationTurn(id=new_id("turn"), thread_id=thread_id, sender_id=current_user_id(), sender_name=user.nickname, body=f"创建了{mode_text}房间，邀请对方一起玩", turn_type="game_room", game_room_id=room.id, created_at=now()))
    thread.last_message = f"创建了{mode_text}房间"
    thread.updated_at = now()
    await session.commit()
    return room.id, await to_thread(session, thread)


async def send_thread_gift(session: AsyncSession, thread_id: str, gift_id: str) -> tuple[WalletState, ConversationThreadOut]:
    user = await get_current_user(session)
    thread = await session.get(ConversationThread, thread_id)
    if thread is None:
        raise HTTPException(status_code=404, detail="THREAD_NOT_FOUND")
    wallet = await send_gift(session, gift_id, thread.user_b_id, "chat", thread_id)
    gift = await session.get(GiftProduct, gift_id)
    session.add(ConversationTurn(id=new_id("turn"), thread_id=thread_id, sender_id=current_user_id(), sender_name=user.nickname, body=f"送出礼物：{gift.name}", turn_type="gift", gift_id=gift_id, created_at=now()))
    thread.last_message = f"送出礼物：{gift.name}"
    thread.updated_at = now()
    await session.commit()
    return wallet, await to_thread(session, thread)


def classify_chat_source(thread: ConversationThread, turns: list[ConversationTurn]) -> str:
    if any(turn.turn_type == "game_room" or turn.game_room_id for turn in turns):
        return "game_room"
    if thread.bottle_id:
        return "bottle"
    if "树洞" in (thread.participant_tag or ""):
        return "treehole"
    return "plaza"


def analyze_chat_discipline(source_type: str, turns: list[ConversationTurn], matched_keywords: list[str]) -> tuple[str, str, list[str]]:
    body_text = "\n".join(turn.body for turn in turns).lower()
    keywords: list[str] = []
    for word in [*matched_keywords, *GAME_DISCIPLINE_WORDS]:
        if word in keywords:
            continue
        if word in matched_keywords or word.lower() in body_text:
            keywords.append(word)

    if source_type == "game_room":
        if keywords:
            return "violation", f"命中游戏房间纪律：{', '.join(keywords[:5])}。", keywords
        return "watch", "游戏房间纪律观察：关注刷屏、辱骂、越界任务和站外导流。", keywords
    if keywords:
        return "violation", f"命中聊天安全关键词：{', '.join(keywords[:5])}。", keywords
    return "clear", "未发现需要处置的聊天纪律问题。", keywords


async def admin_chat_reviews(session: AsyncSession) -> list[AdminChatReviewOut]:
    await get_current_user(session)
    threads = (await session.execute(select(ConversationThread).order_by(desc(ConversationThread.updated_at)))).scalars().all()
    reports = (await session.execute(select(ContentReport).where(ContentReport.target_type == "chat"))).scalars().all()
    reports_by_thread = {report.target_id: report for report in reports}
    rows: list[AdminChatReviewOut] = []
    for thread in threads:
        reporter = reports_by_thread.get(thread.id)
        owner = await session.get(User, thread.user_a_id)
        participant = await session.get(User, thread.user_b_id)
        turns = (await session.execute(select(ConversationTurn).where(ConversationTurn.thread_id == thread.id).order_by(ConversationTurn.created_at))).scalars().all()
        matched_keywords: list[str] = []
        if reporter and reporter.reason.startswith("chat_risk:"):
            matched_keywords = [word for word in reporter.reason.replace("chat_risk:", "").split(",") if word]
        source_type = classify_chat_source(thread, turns)
        discipline_status, discipline_summary, all_keywords = analyze_chat_discipline(source_type, turns, matched_keywords)
        risk_level = "high" if discipline_status == "violation" else "medium" if discipline_status == "watch" else "low"
        room_mode = None
        for turn in turns:
            if not turn.game_room_id:
                continue
            room = await session.get(GameRoom, turn.game_room_id)
            if room:
                room_mode = room.mode
                break
        owner_name = owner.nickname if owner else thread.user_a_id
        participant_name = participant.nickname if participant else thread.participant_name
        owner_avatar_text = owner.avatar_text if owner else None
        owner_avatar_url = owner.avatar_url if owner else None
        participant_avatar_text = participant.avatar_text if participant else None
        participant_avatar_url = participant.avatar_url if participant else None
        if reporter and reporter.status == "reviewing":
            status = "reviewing"
        elif reporter and reporter.status == "resolved":
            status = "resolved"
        elif discipline_status == "violation":
            status = "reviewing"
        elif discipline_status == "watch":
            status = "pending"
        else:
            status = "resolved"
        if source_type == "game_room":
            handling_policy = "游戏房间纪律复核" if discipline_status == "violation" else "游戏房间纪律观察"
        elif all_keywords:
            handling_policy = "聊天关键词脱敏并人工复核"
        else:
            handling_policy = "聊天上下文留存观察"
        reason = discipline_summary
        if reporter and not reporter.reason.startswith("chat_risk:"):
            reason = reporter.reason
        rows.append(AdminChatReviewOut(
            id=reporter.id if reporter else f"chat_review_{thread.id}",
            thread_id=thread.id,
            source=source_type,
            participant_user_ids=[thread.user_a_id, thread.user_b_id],
            participants=[owner_name, participant_name],
            participant_avatar_texts=[owner_avatar_text, participant_avatar_text],
            participant_avatar_urls=[owner_avatar_url, participant_avatar_url],
            related_content=thread.bottle_preview or "",
            last_message=thread.last_message or "",
            risk_level=risk_level,
            status=status,
            review_trigger="keyword" if all_keywords else "risk",
            handling_policy=handling_policy,
            matched_keywords=all_keywords,
            auto_action="mask_and_review" if discipline_status == "violation" else "manual_review",
            reason=reason,
            messages=[await to_turn(session, turn) for turn in turns],
            discipline_status=discipline_status,
            discipline_summary=discipline_summary,
            room_mode=room_mode,
            updated_at=iso(thread.updated_at),
        ))
    return rows


async def verify_membership_order(session: AsyncSession, platform: str, product_id: str, transaction_id: str) -> tuple[MembershipOrderOut, UserProfile]:
    user = await get_current_user(session)
    existing = await session.scalar(select(MembershipOrder).where(MembershipOrder.transaction_id == transaction_id))
    vip_level = {"vip_month": "monthly", "vip_season": "season", "vip_year": "yearly"}.get(product_id, "monthly")
    if existing:
        existing.status = "duplicate_verified"
        await session.commit()
        return membership_order_out(existing), to_user_profile(user)
    order = MembershipOrder(id=new_id("member_order"), user_id=user.id, platform=platform, product_id=product_id, transaction_id=transaction_id, status="mock_verified", vip_level=vip_level, verified_at=now())
    session.add(order)
    user.is_vip = True
    user.vip_level = vip_level
    for quota in (await session.execute(select(QuotaBalance).where(QuotaBalance.user_id == user.id))).scalars().all():
        if quota.vip_bonus < 5:
            quota.remaining += 5 - quota.vip_bonus
            quota.vip_bonus = 5
    await add_notification(session, "会员已开通", "VIP 权益已经生效。", "membership", order.id)
    await session.commit()
    return membership_order_out(order), to_user_profile(user)


async def list_membership_products(session: AsyncSession) -> list[MembershipProduct]:
    await get_current_user(session)
    rows = (
        await session.execute(
            select(MembershipProductConfig).where(MembershipProductConfig.status == "active").order_by(MembershipProductConfig.sort_order)
        )
    ).scalars().all()
    return [
        MembershipProduct(
            id=row.id,
            name=row.name,
            price_label=row.price_label,
            platform=row.platform if row.platform in {"wechat", "ios", "android", "all"} else "all",
            benefits=[item for item in row.benefits_text.splitlines() if item],
        )
        for row in rows
    ]


def membership_order_out(row: MembershipOrder) -> MembershipOrderOut:
    return MembershipOrderOut(id=row.id, platform=row.platform, product_id=row.product_id, transaction_id=row.transaction_id, status=row.status, vip_level=row.vip_level, verified_at=iso(row.verified_at))


async def list_membership_orders(session: AsyncSession) -> list[MembershipOrderOut]:
    await get_current_user(session)
    rows = (await session.execute(select(MembershipOrder).where(MembershipOrder.user_id == current_user_id()).order_by(desc(MembershipOrder.verified_at)))).scalars().all()
    return [membership_order_out(row) for row in rows]


async def admin_counts(session: AsyncSession) -> dict[str, int]:
    await get_current_user(session)
    return {
        "users": await session.scalar(select(func.count(User.id))) or 0,
        "pending_content": (await session.scalar(select(func.count(Bottle.id)).where(Bottle.status == "pending")) or 0)
        + (await session.scalar(select(func.count(TreeholePost.id)).where(TreeholePost.status == "pending")) or 0)
        + (await session.scalar(select(func.count(PlazaPost.id)).where(PlazaPost.status == "pending")) or 0)
        + (await session.scalar(select(func.count(PrivatePhotoAsset.id)).where(PrivatePhotoAsset.status == "pending")) or 0),
        "reports": await session.scalar(select(func.count(ContentReport.id))) or 0,
        "ad_rewards_today": await session.scalar(select(func.count(AdRewardSession.id)).where(AdRewardSession.status == "settled")) or 0,
        "orders_today": await session.scalar(select(func.count(PaymentOrder.id)).where(PaymentOrder.status == "paid")) or 0,
    }


async def _latest_restriction_map(session: AsyncSession, user_ids: list[str]) -> dict[str, AdminUserRestriction]:
    if not user_ids:
        return {}
    rows = (
        await session.execute(
            select(AdminUserRestriction)
            .where(AdminUserRestriction.user_id.in_(user_ids))
            .order_by(AdminUserRestriction.user_id, desc(AdminUserRestriction.updated_at))
        )
    ).scalars().all()
    restriction_by_user: dict[str, AdminUserRestriction] = {}
    for row in rows:
        if row.user_id not in restriction_by_user:
            restriction_by_user[row.user_id] = row
    return restriction_by_user


async def _user_map(session: AsyncSession, user_ids: list[str]) -> dict[str, User]:
    if not user_ids:
        return {}
    users = (
        await session.execute(
            select(User).where(User.id.in_(user_ids))
        )
    ).scalars().all()
    return {user.id: user for user in users}


async def admin_users(session: AsyncSession) -> list[tuple[User, AdminUserRestriction | None]]:
    await get_current_user(session)
    users = (await session.execute(select(User).order_by(User.created_at))).scalars().all()
    restrictions = await _latest_restriction_map(session, [user.id for user in users])
    return [(user, restrictions.get(user.id)) for user in users]


async def update_user_status(
    session: AsyncSession,
    user_id: str,
    status: str,
    reason: str | None = None,
    block_days: int | None = None,
    blocked_until: str | None = None,
) -> tuple[User, AdminUserRestriction | None]:
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="USER_NOT_FOUND")
    if status not in {"active", "limited", "blocked"}:
        raise HTTPException(status_code=422, detail="INVALID_STATUS")

    restrictions = await _latest_restriction_map(session, [user.id])
    restriction = restrictions.get(user.id)
    now_ts = now()

    if status == "blocked":
        blocked_until_at = _coerce_blocked_until(blocked_until, block_days)
        if restriction:
            restriction.status = "blocked"
            restriction.reason = reason or restriction.reason
            restriction.blocked_until = blocked_until_at
            restriction.updated_at = now_ts
        else:
            session.add(
                AdminUserRestriction(
                    id=new_id("admin_restriction"),
                    user_id=user.id,
                    status="blocked",
                    reason=reason,
                    blocked_until=blocked_until_at,
                    action_by=None,
                    created_at=now_ts,
                    updated_at=now_ts,
                )
            )
        user.status = "blocked"
    else:
        user.status = status
        if restriction:
            restriction.status = status
            restriction.reason = reason or restriction.reason
            restriction.blocked_until = None
            restriction.updated_at = now_ts

    user.status = status
    await session.commit()
    if status == "blocked":
        if restriction is None:
            restriction = await session.scalar(
                select(AdminUserRestriction)
                .where(AdminUserRestriction.user_id == user.id)
                .order_by(desc(AdminUserRestriction.updated_at))
                .limit(1)
            )
    else:
        restriction = await session.scalar(
            select(AdminUserRestriction)
            .where(AdminUserRestriction.user_id == user.id)
            .order_by(desc(AdminUserRestriction.updated_at))
            .limit(1)
        )
    return user, restriction


async def admin_content_rows(
    session: AsyncSession,
) -> list[tuple[str, str, str, str, str | None, str | None, str | None, str, datetime]]:
    await get_current_user(session)
    rows: list[tuple[str, str, str, str, str | None, str | None, str | None, str, datetime]] = []
    content_sources = [
        ("bottle", select(Bottle)),
        ("treehole", select(TreeholePost)),
        ("plaza", select(PlazaPost)),
        ("private_photo", select(PrivatePhotoAsset)),
    ]
    for source_type, query in content_sources:
        for item in (await session.execute(query)).scalars().all():
            if source_type == "bottle":
                author_id = item.author_id
                author_name = item.author_name
                author_avatar_text = item.author_avatar_text
                author_avatar_url = None
                excerpt = item.content[:60]
                status_value = item.status
            elif source_type == "treehole":
                author_id = item.author_id
                author_name = item.author_name
                author_avatar_text = item.author_avatar_text
                author_avatar_url = item.author_avatar_url
                excerpt = item.content[:60]
                status_value = item.status
            elif source_type == "plaza":
                author_id = item.author_id
                author_name = item.author_name
                author_avatar_text = None
                author_avatar_url = None
                excerpt = (item.content[:60] if item.content else "")
                status_value = item.status
            else:
                author_id = item.owner_id
                author_name = item.owner_name
                author_avatar_text = None
                author_avatar_url = None
                excerpt = (item.title if item.title else item.owner_name)[:60]
                status_value = {
                    "ai_approved": "approved",
                    "manual_approved": "approved",
                    "approved": "approved",
                    "rejected": "rejected",
                    "frozen": "rejected",
                }.get(item.status, "pending")
            rows.append((item.id, source_type, status_value, author_id, author_name, author_avatar_text, author_avatar_url, excerpt, item.created_at))

    user_ids = {author_id for _, _, _, author_id, _, _, _, _, _ in rows}
    users = await _user_map(session, list(user_ids))
    rows.sort(key=lambda row: row[-1], reverse=True)

    enriched: list[tuple[str, str, str, str, str | None, str | None, str | None, str, datetime]] = []
    for row_id, source_type, status_value, author_id, fallback_author_name, fallback_avatar_text, fallback_avatar_url, excerpt, created_at in rows:
        row_author = users.get(author_id)
        enriched.append(
            (
                row_id,
                source_type,
                status_value,
                author_id,
                row_author.nickname if row_author else fallback_author_name,
                row_author.avatar_text if row_author and row_author.avatar_text else fallback_avatar_text,
                row_author.avatar_url if row_author and row_author.avatar_url else fallback_avatar_url,
                excerpt,
                created_at,
            )
        )
    return enriched


async def audit(session: AsyncSession, actor: str, action: str, target_type: str, target_id: str, detail: str | None = None) -> None:
    session.add(AdminAuditLog(id=new_id("audit"), actor=actor, action=action, target_type=target_type, target_id=target_id, detail=detail, created_at=now()))
    await session.commit()


async def list_audit(session: AsyncSession):
    await get_current_user(session)
    return (await session.execute(select(AdminAuditLog).order_by(desc(AdminAuditLog.created_at)))).scalars().all()
