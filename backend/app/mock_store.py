from copy import deepcopy
from datetime import UTC, datetime
from random import choice
from uuid import uuid4

from fastapi import HTTPException

from app.schemas import (
    AdRewardState,
    AdminRewardConfig,
    BottleOut,
    CheckinState,
    ContentStatus,
    DareTaskOut,
    BlockOut,
    MembershipOrderOut,
    MeStatus,
    QuotaItem,
    QuotaType,
    ReportOut,
    TreeholePostOut,
    TruthQuestionOut,
    UserProfile,
)

QUOTA_LABELS = {
    QuotaType.fish_bottle: "捞瓶",
    QuotaType.throw_bottle: "扔瓶",
    QuotaType.truth: "真心话",
    QuotaType.dare: "大冒险",
    QuotaType.treehole_post: "树洞",
}

BASE_QUOTAS = {
    QuotaType.fish_bottle: 5,
    QuotaType.throw_bottle: 3,
    QuotaType.truth: 3,
    QuotaType.dare: 3,
    QuotaType.treehole_post: 2,
}

VIP_BONUS = {
    QuotaType.fish_bottle: 5,
    QuotaType.throw_bottle: 3,
    QuotaType.truth: 3,
    QuotaType.dare: 3,
    QuotaType.treehole_post: 2,
}

CHECKIN_REWARDS = [10, 10, 30, 10, 10, 30, 100]

BOTTLE_PROMPT_TEMPLATES = [
    "今天有什么小事让你觉得还不错？",
    "如果今晚可以不用考虑明天，你最想做什么？",
    "推荐我一个你最近喜欢的歌、电影或小店吧。",
    "你最近有没有一个瞬间，突然觉得自己被生活温柔了一下？",
    "如果把今天的心情取一个天气名字，你会叫它什么？",
    "我这里有一点海风，想换你一句今天的故事。",
    "你会因为什么样的小细节，对一个陌生人多一点好感？",
    "最近有没有一个让你忍不住笑出来的瞬间？",
    "如果现在能收到一份小礼物，你希望它是什么？",
    "你喜欢慢慢熟悉的人，还是一开始就很有默契的人？",
    "今天辛苦了，愿意把最想被理解的一句话丢进这个瓶子吗？",
    "如果今晚有人认真听你说话，你最想先说哪一句？",
    "你心里有没有一个想去很久、但还没出发的地方？",
    "你觉得一个舒服的聊天，最重要的是什么？",
    "如果把烦恼折成纸船，你想让它漂去哪里？",
    "最近让你觉得有点期待的事情是什么？",
    "你喜欢被怎样温柔地关心？",
    "如果可以给陌生人留一句好运，你会写什么？",
]


def iso_now() -> str:
    return datetime.now(UTC).isoformat()


user = UserProfile(
    id="user_mock_001",
    nickname="海风来信",
    avatar_text="海",
    platform="wechat",
    is_vip=True,
    vip_level="monthly",
    vip_expires_at="2026-07-25T23:59:59+08:00",
    drift_coins=260,
    gender="female",
    city="杭州",
)

quotas = {
    quota_type: QuotaItem(
        type=quota_type,
        label=QUOTA_LABELS[quota_type],
        base=base,
        vip_bonus=VIP_BONUS[quota_type],
        ad_bonus=0,
        used=0,
        remaining=base + VIP_BONUS[quota_type],
    )
    for quota_type, base in BASE_QUOTAS.items()
}

ad_reward = AdRewardState(can_watch=True, cooldown_seconds=0, cooldown_minutes=30, reward_per_quota=1)
checkin = CheckinState(checked_today=False, streak_days=2, week_rewards=CHECKIN_REWARDS, current_week_index=2)
settled_ad_sessions: set[str] = set()
consumed_business_ids: set[str] = set()
reacted_treehole_ids: set[str] = set()
orders_by_transaction: dict[str, MembershipOrderOut] = {}
reports_by_key: dict[str, ReportOut] = {}
blocks_by_user: dict[str, BlockOut] = {}
following_user_ids: set[str] = set()
last_fished_bottle_id: str | None = None
last_fished_author_id: str | None = None

NEARBY_CITY_MAP = {
    "杭州": ["杭州", "上海", "宁波", "苏州"],
    "上海": ["上海", "杭州", "苏州", "南京"],
    "广州": ["广州", "深圳", "佛山"],
    "深圳": ["深圳", "广州", "东莞"],
    "北京": ["北京", "天津"],
    "成都": ["成都", "重庆"],
}

bottles = [
    BottleOut(
        id="bottle_001",
        author_name="海岛来信",
        author_id="creator_001",
        author_avatar_text="海",
        author_vip=True,
        author_gender="female",
        author_age_range="25-30",
        author_city="上海",
        author_verified=True,
        content="今天把想说的话写进瓶子里，希望捞到的人刚好也需要一点安静。",
        mood="平静",
        status="approved",
        replies=5,
        target_gender="all",
        target_scope="all",
        created_at=iso_now(),
    ),
    BottleOut(
        id="bottle_002",
        author_id="creator_002",
        author_name="晚风",
        author_avatar_text="晚",
        author_vip=False,
        author_gender="female",
        author_age_range="18-24",
        author_city="杭州",
        author_verified=True,
        content="如果你正在犹豫要不要重新开始，我想把勇气分你一点。",
        mood="鼓励",
        status="approved",
        replies=2,
        target_gender="all",
        target_scope="all",
        created_at=iso_now(),
    ),
    BottleOut(
        id="bottle_003",
        author_id="creator_003",
        author_name="北岸",
        author_avatar_text="北",
        author_vip=False,
        author_gender="male",
        author_age_range="25-30",
        author_city="杭州",
        author_verified=True,
        content="刚下班路过江边，突然觉得今天也不是完全糟糕，至少风很舒服。",
        mood="放松",
        status="approved",
        replies=1,
        target_gender="all",
        target_scope="same_city",
        created_at=iso_now(),
    ),
    BottleOut(
        id="bottle_004",
        author_id="creator_004",
        author_name="小满",
        author_avatar_text="满",
        author_vip=True,
        author_gender="female",
        author_age_range="22-26",
        author_city="成都",
        author_verified=True,
        content="希望捞到这个瓶子的人，今天可以少一点内耗，多一点被认真对待的感觉。",
        mood="温柔",
        status="approved",
        replies=8,
        target_gender="all",
        target_scope="all",
        created_at=iso_now(),
    ),
    BottleOut(
        id="bottle_005",
        author_id="creator_005",
        author_name="凌晨三点",
        author_avatar_text="凌",
        author_vip=False,
        author_gender="male",
        author_age_range="30-35",
        author_city="深圳",
        author_verified=False,
        content="有时候不是想聊天，只是想知道世界上还有人也醒着。",
        mood="深夜",
        status="approved",
        replies=3,
        target_gender="all",
        target_scope="all",
        created_at=iso_now(),
    ),
    BottleOut(
        id="bottle_006",
        author_id="creator_006",
        author_name="蓝莓气泡",
        author_avatar_text="蓝",
        author_vip=True,
        author_gender="female",
        author_age_range="18-24",
        author_city="广州",
        author_verified=True,
        content="今天被一句很小的话治愈了，也想把这份轻松传给你。",
        mood="开心",
        status="approved",
        replies=12,
        target_gender="all",
        target_scope="same_city",
        created_at=iso_now(),
    ),
    BottleOut(
        id="bottle_007",
        author_id="creator_007",
        author_name="山月",
        author_avatar_text="山",
        author_vip=False,
        author_gender="female",
        author_age_range="27-32",
        author_city="北京",
        author_verified=True,
        content="如果你也正在重新整理生活，我们可以各自安静努力，然后在海上碰一下杯。",
        mood="自洽",
        status="approved",
        replies=6,
        target_gender="all",
        target_scope="all",
        created_at=iso_now(),
    ),
    BottleOut(
        id="bottle_008",
        author_id="creator_008",
        author_name="南窗",
        author_avatar_text="南",
        author_vip=False,
        author_gender="unknown",
        author_age_range="未知",
        author_city="厦门",
        author_verified=False,
        content="把一个没法说出口的问题丢进海里，希望明天醒来能轻一点。",
        mood="树洞",
        status="approved",
        replies=0,
        target_gender="all",
        target_scope="all",
        created_at=iso_now(),
    )
]

treeholes = [
    TreeholePostOut(
        id="tree_001",
        content="有些话不想让熟人看见，但憋在心里又太重了。",
        resonance_count=42,
        reply_count=8,
        status="approved",
        created_at=iso_now(),
    )
]

truth_questions = [
    TruthQuestionOut(id="truth_001", category="情感", text="你最近一次真正心动，是因为什么细节？"),
    TruthQuestionOut(id="truth_002", category="朋友局", text="你最希望朋友理解你哪一点？"),
]

dare_tasks = [
    DareTaskOut(id="dare_001", category="轻松", text="给今天的自己写一句夸奖，并保存下来。"),
    DareTaskOut(id="dare_002", category="社交", text="向一个很久没联系的人发一句问候。"),
]


def get_status() -> MeStatus:
    return MeStatus(user=deepcopy(user), quotas=deepcopy(quotas), ad_reward=deepcopy(ad_reward), checkin=deepcopy(checkin))


def consume_quota(quota_type: QuotaType, business_id: str) -> QuotaItem:
    if business_id in consumed_business_ids:
        return quotas[quota_type]
    quota = quotas[quota_type]
    if quota.remaining <= 0:
        raise HTTPException(status_code=409, detail="QUOTA_NOT_ENOUGH")
    quota.used += 1
    quota.remaining -= 1
    consumed_business_ids.add(business_id)
    return quota


def checkin_today() -> CheckinState:
    global user
    if checkin.checked_today:
        return checkin
    reward = checkin.week_rewards[checkin.current_week_index]
    user.drift_coins += reward
    checkin.checked_today = True
    checkin.streak_days += 1
    checkin.last_reward = reward
    checkin.current_week_index = checkin.streak_days % len(checkin.week_rewards)
    return checkin


def prepare_ad_reward() -> str:
    if not ad_reward.can_watch:
        raise HTTPException(status_code=409, detail="AD_COOLDOWN")
    session_id = f"ad_{uuid4().hex}"
    ad_reward.active_session_id = session_id
    return session_id


def commit_ad_reward(session_id: str, completed: bool) -> MeStatus:
    if not completed:
        raise HTTPException(status_code=409, detail="AD_NOT_COMPLETED")
    if session_id not in settled_ad_sessions:
        settled_ad_sessions.add(session_id)
        for quota in quotas.values():
            quota.ad_bonus += ad_reward.reward_per_quota
            quota.remaining += ad_reward.reward_per_quota
        ad_reward.can_watch = False
        ad_reward.cooldown_seconds = ad_reward.cooldown_minutes * 60
    return get_status()


def create_bottle(content: str, target_gender: str = "all", target_scope: str = "all") -> BottleOut:
    content = content.strip()
    if not content:
        raise HTTPException(status_code=422, detail="EMPTY_BOTTLE_CONTENT")
    consume_quota(QuotaType.throw_bottle, f"throw:{uuid4().hex}")
    bottle = BottleOut(
        id=f"bottle_{uuid4().hex}",
        author_id=user.id,
        author_name=user.nickname,
        author_avatar_text=user.avatar_text,
        author_vip=user.is_vip,
        author_gender=user.gender,
        author_age_range="25-30",
        author_city=user.city or "全国",
        author_verified=bool(user.face_verified and user.gender_verified),
        content=content,
        mood="待审核",
        status="pending",
        replies=0,
        target_gender=target_gender,
        target_scope=target_scope,
        created_at=iso_now(),
    )
    bottles.insert(0, bottle)
    return bottle


def random_bottle_prompt() -> str:
    return choice(BOTTLE_PROMPT_TEMPLATES)


def list_bottles() -> list[BottleOut]:
    result = []
    for item in bottles:
        bottle = deepcopy(item)
        bottle.is_following = bottle.author_id in following_user_ids
        result.append(bottle)
    return result


def is_nearby_city(author_city: str | None, current_city: str | None = None) -> bool:
    city = current_city or user.city
    if not author_city or not city or city == "全国":
        return False
    return author_city in NEARBY_CITY_MAP.get(city, [city])


def bottle_allows_viewer(item: BottleOut) -> bool:
    if item.target_gender != "all" and item.target_gender != user.gender:
        return False
    if item.target_scope == "same_city":
        return item.author_city == user.city
    if item.target_scope == "nearby":
        return is_nearby_city(item.author_city)
    return True


def bottle_matches_filter(
    item: BottleOut,
    city: str | None = None,
    gender: str | None = None,
    age_range: str | None = None,
) -> bool:
    if city == "同城" and item.author_city != user.city:
        return False
    if city == "附近" and not is_nearby_city(item.author_city):
        return False
    if gender == "女" and item.author_gender != "female":
        return False
    if gender == "男" and item.author_gender != "male":
        return False
    if age_range and age_range != "全部" and item.author_age_range != age_range:
        return False
    return True


def fish_bottle(city: str | None = None, gender: str | None = None, age_range: str | None = None) -> BottleOut:
    global last_fished_author_id, last_fished_bottle_id
    available = [
        item
        for item in bottles
        if item.status != ContentStatus.rejected
        and item.author_id != user.id
        and bottle_allows_viewer(item)
        and bottle_matches_filter(item, city=city, gender=gender, age_range=age_range)
    ]
    if not available:
        raise HTTPException(status_code=404, detail="BOTTLE_NOT_FOUND")

    candidates = [
        item for item in available if item.id != last_fished_bottle_id and item.author_id != last_fished_author_id
    ]
    if not candidates:
        candidates = [item for item in available if item.id != last_fished_bottle_id]
    if not candidates:
        candidates = available

    bottle = deepcopy(choice(candidates))
    consume_quota(QuotaType.fish_bottle, f"fish:{uuid4().hex}")
    bottle.is_following = bottle.author_id in following_user_ids
    last_fished_bottle_id = bottle.id
    last_fished_author_id = bottle.author_id
    return bottle


def create_treehole(content: str) -> TreeholePostOut:
    consume_quota(QuotaType.treehole_post, f"tree:{uuid4().hex}")
    post = TreeholePostOut(
        id=f"tree_{uuid4().hex}",
        content=content,
        resonance_count=0,
        reply_count=0,
        status="pending",
        created_at=iso_now(),
    )
    treeholes.insert(0, post)
    return post


def react_treehole(post_id: str) -> TreeholePostOut | None:
    post = next((item for item in treeholes if item.id == post_id), None)
    if post is None:
        return None
    if post_id not in reacted_treehole_ids:
        post.resonance_count += 1
        reacted_treehole_ids.add(post_id)
    return post


def verify_membership_order(platform: str, product_id: str, transaction_id: str) -> MembershipOrderOut:
    if transaction_id in orders_by_transaction:
        order = orders_by_transaction[transaction_id]
        order.status = "duplicate_verified"
        return order

    vip_level = "monthly"
    if "season" in product_id:
        vip_level = "season"
    if "year" in product_id:
        vip_level = "yearly"

    order = MembershipOrderOut(
        id=f"order_{uuid4().hex}",
        platform=platform,
        product_id=product_id,
        transaction_id=transaction_id,
        status="mock_verified",
        vip_level=vip_level,
        verified_at=iso_now(),
    )
    orders_by_transaction[transaction_id] = order
    user.is_vip = True
    user.vip_level = vip_level
    return order


def create_report(target_type: str, target_id: str, reason: str) -> ReportOut:
    key = f"{target_type}:{target_id}:{reason}"
    if key not in reports_by_key:
        reports_by_key[key] = ReportOut(
            id=f"report_{uuid4().hex}",
            target_type=target_type,
            target_id=target_id,
            reason=reason,
            status="queued",
            created_at=iso_now(),
        )
    return reports_by_key[key]


def block_user(blocked_user_id: str) -> BlockOut:
    if blocked_user_id not in blocks_by_user:
        blocks_by_user[blocked_user_id] = BlockOut(
            id=f"block_{uuid4().hex}",
            blocked_user_id=blocked_user_id,
            status="blocked",
            blocked_at=iso_now(),
        )
    return blocks_by_user[blocked_user_id]


def get_reward_config() -> AdminRewardConfig:
    return AdminRewardConfig(
        base_quotas=BASE_QUOTAS,
        vip_bonus=VIP_BONUS,
        ad_cooldown_minutes=ad_reward.cooldown_minutes,
        ad_reward_per_quota=ad_reward.reward_per_quota,
        checkin_rewards=CHECKIN_REWARDS,
    )
