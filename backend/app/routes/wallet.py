from fastapi import APIRouter, HTTPException

from app.mock_store import iso_now
from app.schemas import (
    BlacklistItem,
    CoinLedgerItem,
    CreatorProfile,
    GiftProduct,
    GiftSendResponse,
    NearbyUser,
    PhotoUnlockResponse,
    PlazaPost,
    PlazaCommentOut,
    PlazaMediaOut,
    PrivatePhoto,
    ReferralClaimResponse,
    ReferralState,
    SendGiftRequest,
    UnlockPhotoRequest,
    VerificationState,
    VerificationOverview,
    WalletOverview,
    WalletState,
    WithdrawRequest,
    WithdrawResponse,
)

router = APIRouter(tags=["wallet"])

wallet = WalletState(
    recharge_coins=520,
    earned_coins=180,
    gift_coins=68,
    withdrawable_coins=180,
    frozen_coins=20,
    charm_value=1880,
    withdraw_threshold_charm=1000,
    charm_exchange_rate=100,
)
ledger = [
    CoinLedgerItem(id="ledger_001", title="私密照片被查看", amount=30, coin_bucket="earned", withdrawable=True, created_at=iso_now()),
    CoinLedgerItem(id="ledger_002", title="充值金币", amount=200, coin_bucket="recharge", withdrawable=False, created_at=iso_now()),
]
creators = [
    CreatorProfile(user_id="creator_001", display_name="海岛来信", gender="female", verified=True, safety_score=96, follower_count=1280, album_count=3, earned_coins=360, charm_value=3600),
    CreatorProfile(user_id="creator_002", display_name="晚风", gender="female", verified=True, safety_score=91, follower_count=840, album_count=2, earned_coins=180, charm_value=1800),
]
photos = [
    PrivatePhoto(id="photo_001", owner_id="creator_001", owner_name="海岛来信", title="今日海边碎片", price_coins=30, status="approved", purchased=False),
    PrivatePhoto(id="photo_002", owner_id="creator_002", owner_name="晚风", title="只给认真回应的人看", price_coins=20, status="approved", purchased=False),
]
gifts = [
    GiftProduct(id="gift_shell", name="贝壳", price_coins=10, icon_text="贝"),
    GiftProduct(id="gift_star", name="星光", price_coins=30, icon_text="星"),
    GiftProduct(id="gift_bottle", name="玻璃瓶", price_coins=68, icon_text="瓶"),
]
verification = VerificationState(face_verified=True, gender_verified=True, detected_gender="female", liveness_passed=True, manual_review_status="approved")
referral = ReferralState(invite_code="SEA260", invited_count=3, reward_vip_days=7, next_reward_need=5)
blacklist = [BlacklistItem(id="block_001", user_id="bad_user_001", nickname="无礼访客", reason="骚扰私信", blocked_at=iso_now())]
plaza_media = [
    PlazaMediaOut(
        id="plaza_media_001",
        post_id="plaza_001",
        owner_id="creator_001",
        media_type="image",
        url="https://picsum.photos/id/1011/900/1200",
        storage_key="remote/picsum/1011-900x1200.jpg",
        mime_type="image/jpeg",
        size_bytes=428000,
        width=1200,
        height=1600,
        created_at=iso_now(),
    ),
    PlazaMediaOut(
        id="plaza_media_002",
        post_id="plaza_001",
        owner_id="creator_001",
        media_type="image",
        url="https://picsum.photos/id/1027/900/1200",
        storage_key="remote/picsum/1027-900x1200.jpg",
        mime_type="image/jpeg",
        size_bytes=392000,
        width=1200,
        height=1600,
        created_at=iso_now(),
    ),
    PlazaMediaOut(
        id="plaza_media_005",
        post_id="plaza_001",
        owner_id="creator_001",
        media_type="image",
        url="https://picsum.photos/id/1035/900/1200",
        storage_key="remote/picsum/1035-900x1200.jpg",
        mime_type="image/jpeg",
        size_bytes=376000,
        width=1200,
        height=1600,
        created_at=iso_now(),
    ),
    PlazaMediaOut(
        id="plaza_media_006",
        post_id="plaza_001",
        owner_id="creator_001",
        media_type="image",
        url="https://picsum.photos/id/1040/900/1200",
        storage_key="remote/picsum/1040-900x1200.jpg",
        mime_type="image/jpeg",
        size_bytes=401000,
        width=1200,
        height=1600,
        created_at=iso_now(),
    ),
    PlazaMediaOut(
        id="plaza_media_007",
        post_id="plaza_001",
        owner_id="creator_001",
        media_type="image",
        url="https://picsum.photos/id/1043/900/1200",
        storage_key="remote/picsum/1043-900x1200.jpg",
        mime_type="image/jpeg",
        size_bytes=384000,
        width=1200,
        height=1600,
        created_at=iso_now(),
    ),
    PlazaMediaOut(
        id="plaza_media_008",
        post_id="plaza_001",
        owner_id="creator_001",
        media_type="image",
        url="https://picsum.photos/id/1056/900/1200",
        storage_key="remote/picsum/1056-900x1200.jpg",
        mime_type="image/jpeg",
        size_bytes=418000,
        width=1200,
        height=1600,
        created_at=iso_now(),
    ),
    PlazaMediaOut(
        id="plaza_media_009",
        post_id="plaza_001",
        owner_id="creator_001",
        media_type="image",
        url="https://picsum.photos/id/1062/900/1200",
        storage_key="remote/picsum/1062-900x1200.jpg",
        mime_type="image/jpeg",
        size_bytes=396000,
        width=1200,
        height=1600,
        created_at=iso_now(),
    ),
    PlazaMediaOut(
        id="plaza_media_010",
        post_id="plaza_001",
        owner_id="creator_001",
        media_type="image",
        url="https://picsum.photos/id/1068/900/1200",
        storage_key="remote/picsum/1068-900x1200.jpg",
        mime_type="image/jpeg",
        size_bytes=389000,
        width=1200,
        height=1600,
        created_at=iso_now(),
    ),
    PlazaMediaOut(
        id="plaza_media_011",
        post_id="plaza_001",
        owner_id="creator_001",
        media_type="image",
        url="https://picsum.photos/id/1074/900/1200",
        storage_key="remote/picsum/1074-900x1200.jpg",
        mime_type="image/jpeg",
        size_bytes=407000,
        width=1200,
        height=1600,
        created_at=iso_now(),
    ),
    PlazaMediaOut(
        id="plaza_media_003",
        post_id="plaza_002",
        owner_id="creator_003",
        media_type="voice",
        url="https://interactive-examples.mdn.mozilla.net/media/cc0-audio/t-rex-roar.mp3",
        storage_key="remote/mdn/t-rex-roar.mp3",
        mime_type="audio/mpeg",
        size_bytes=39868,
        duration_seconds=2,
        created_at=iso_now(),
    ),
    PlazaMediaOut(
        id="plaza_media_004",
        post_id="plaza_003",
        owner_id="creator_006",
        media_type="video",
        url="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
        storage_key="remote/mdn/flower.mp4",
        mime_type="video/mp4",
        size_bytes=1128375,
        duration_seconds=5,
        width=1080,
        height=1920,
        created_at=iso_now(),
    ),
]
plaza_posts = [
    PlazaPost(
        id="plaza_001",
        author_id="creator_001",
        author_name="海岛来信",
        icon_text="证",
        topic="今日心情",
        content="今晚想收一只认真写的动态，也想把好运分给路过的人。",
        media_type="image",
        media_count=9,
        gender="female",
        verified=True,
        city="上海",
        age_range="25-30",
        view_count=1680,
        like_count=328,
        comment_count=42,
        comment_preview="这条动态很舒服。",
        media=[item for item in plaza_media if item.post_id == "plaza_001"],
        distance_text="同城",
        created_at=iso_now(),
    ),
    PlazaPost(
        id="plaza_002",
        author_id="creator_003",
        author_name="北岸",
        icon_text="近",
        topic="附近动态",
        content="附近 2km 有人分享了今天的晚风和一家新开的甜品店。",
        media_type="voice",
        media_count=1,
        gender="male",
        verified=True,
        city="杭州",
        age_range="25-30",
        view_count=520,
        like_count=89,
        comment_count=17,
        comment_preview="甜品店在哪一条街？",
        media=[item for item in plaza_media if item.post_id == "plaza_002"],
        distance_text="2.1km",
        created_at=iso_now(),
    ),
    PlazaPost(
        id="plaza_003",
        author_id="creator_006",
        author_name="蓝莓气泡",
        icon_text="蓝",
        topic="新人推荐",
        content="拍了一段傍晚路灯亮起来的视频，感觉今天也有一点值得被记住。",
        media_type="video",
        media_count=1,
        gender="female",
        verified=True,
        city="广州",
        age_range="18-24",
        view_count=260,
        like_count=146,
        comment_count=9,
        comment_preview="这个傍晚很有氛围。",
        media=[item for item in plaza_media if item.post_id == "plaza_003"],
        distance_text="新人",
        created_at=iso_now(),
    ),
]
plaza_comments = [
    PlazaCommentOut(
        id="plaza_comment_001",
        post_id="plaza_001",
        author_id="user_mock_001",
        author_name="海风来信",
        icon_text="海",
        author_gender="female",
        author_age_range="25-30",
        author_verified=False,
        author_city="杭州",
        content="这条动态很舒服。",
        hidden_for_owner_only=False,
        created_at=iso_now(),
    ),
    PlazaCommentOut(
        id="plaza_comment_002",
        post_id="plaza_002",
        author_id="creator_002",
        author_name="晚风",
        icon_text="晚",
        author_gender="female",
        author_age_range="18-24",
        author_verified=True,
        author_city="杭州",
        content="甜品店在哪一条街？",
        hidden_for_owner_only=False,
        created_at=iso_now(),
    ),
    PlazaCommentOut(
        id="plaza_comment_003",
        post_id="plaza_003",
        author_id="creator_001",
        author_name="海岛来信",
        icon_text="证",
        author_gender="female",
        author_age_range="25-30",
        author_verified=True,
        author_city="上海",
        content="这个傍晚很有氛围。",
        hidden_for_owner_only=False,
        created_at=iso_now(),
    ),
    PlazaCommentOut(
        id="plaza_comment_004",
        post_id="plaza_001",
        author_id="creator_002",
        author_name="晚风",
        icon_text="晚",
        author_gender="female",
        author_age_range="18-24",
        author_verified=True,
        author_city="杭州",
        content="这条只想给发布者看到。",
        hidden_for_owner_only=True,
        visible_to_owner_only=True,
        created_at=iso_now(),
    ),
    PlazaCommentOut(
        id="plaza_comment_005",
        post_id="plaza_001",
        author_id="creator_005",
        author_name="小满",
        icon_text="满",
        author_gender="female",
        author_age_range="22-26",
        author_verified=True,
        author_city="成都",
        content="我也想把今天收好，明天再慢慢打开。",
        hidden_for_owner_only=False,
        created_at=iso_now(),
    ),
    PlazaCommentOut(
        id="plaza_comment_006",
        post_id="plaza_001",
        author_id="creator_007",
        author_name="橘子海",
        icon_text="橘",
        author_gender="female",
        author_age_range="27-32",
        author_verified=True,
        author_city="北京",
        content="这条隐藏留言只给发布者看，路过的人不会看到。",
        hidden_for_owner_only=True,
        visible_to_owner_only=True,
        created_at=iso_now(),
    ),
    PlazaCommentOut(
        id="plaza_comment_007",
        post_id="plaza_002",
        author_id="creator_008",
        author_name="阿树",
        icon_text="树",
        author_gender="unknown",
        author_age_range="未知",
        author_verified=False,
        author_city="厦门",
        content="如果是晚上去，记得点靠窗的位置。",
        hidden_for_owner_only=False,
        created_at=iso_now(),
    ),
    PlazaCommentOut(
        id="plaza_comment_008",
        post_id="plaza_003",
        author_id="creator_009",
        author_name="南风",
        icon_text="南",
        author_gender="male",
        author_age_range="25-30",
        author_verified=False,
        author_city="深圳",
        content="这个视频适合配一首很轻的歌。",
        hidden_for_owner_only=False,
        created_at=iso_now(),
    ),
]
nearby_users = [
    NearbyUser(id="near_001", nickname="海岛来信", icon_text="证", gender="female", verified=True, age_range="25-30", distance_km=1.2, distance_text="1.2km", signature="只接受礼貌的关注和好友申请。", is_vip=True, online=True),
    NearbyUser(id="near_002", nickname="北岸", icon_text="近", gender="male", verified=True, age_range="25-30", distance_km=2.8, distance_text="2.8km", signature="喜欢听故事，也认真回瓶子。", is_vip=False, online=False),
]


@router.get("/wallet", response_model=WalletOverview)
def get_wallet() -> WalletOverview:
    return WalletOverview(wallet=wallet, ledger=ledger, gifts=gifts)


@router.get("/creators", response_model=list[CreatorProfile])
def list_creators() -> list[CreatorProfile]:
    return creators


@router.get("/verification", response_model=VerificationOverview)
def get_verification() -> VerificationOverview:
    return VerificationOverview(verification=verification, referral=referral)


@router.post("/verification/face")
def submit_face_verification() -> VerificationState:
    verification.face_verified = True
    verification.gender_verified = True
    verification.liveness_passed = True
    verification.detected_gender = "female"
    verification.manual_review_status = "pending"
    return verification


@router.post("/referrals/claim-vip", response_model=ReferralClaimResponse)
def claim_referral_vip() -> ReferralClaimResponse:
    if referral.invited_count < referral.next_reward_need:
        return ReferralClaimResponse(status="not_enough", referral=referral)
    return ReferralClaimResponse(status="claimed", referral=referral)


@router.get("/blacklist", response_model=list[BlacklistItem])
def list_blacklist() -> list[BlacklistItem]:
    return blacklist


@router.get("/private-photos", response_model=list[PrivatePhoto])
def list_private_photos() -> list[PrivatePhoto]:
    return photos


@router.post("/private-photos/unlock", response_model=PhotoUnlockResponse)
def unlock_private_photo(payload: UnlockPhotoRequest) -> PhotoUnlockResponse:
    photo = next((item for item in photos if item.id == payload.photo_id), None)
    if photo is None:
        raise HTTPException(status_code=404, detail="PHOTO_NOT_FOUND")
    if not photo.purchased:
        if wallet.recharge_coins < photo.price_coins:
            raise HTTPException(status_code=409, detail="COIN_NOT_ENOUGH")
        wallet.recharge_coins -= photo.price_coins
        photo.purchased = True
    return PhotoUnlockResponse(photo=photo, wallet=wallet)


@router.post("/gifts/send", response_model=GiftSendResponse)
def send_gift(payload: SendGiftRequest) -> GiftSendResponse:
    gift = next((item for item in gifts if item.id == payload.gift_id), None)
    if gift is None:
        raise HTTPException(status_code=404, detail="GIFT_NOT_FOUND")
    if wallet.recharge_coins < gift.price_coins:
        raise HTTPException(status_code=409, detail="COIN_NOT_ENOUGH")
    wallet.recharge_coins -= gift.price_coins
    return GiftSendResponse(status="sent", receiver_id=payload.receiver_id, wallet=wallet)


@router.post("/wallet/withdraw", response_model=WithdrawResponse)
def request_withdraw(payload: WithdrawRequest) -> WithdrawResponse:
    required_charm = payload.amount * wallet.charm_exchange_rate
    if wallet.charm_value < wallet.withdraw_threshold_charm or required_charm > wallet.charm_value:
        raise HTTPException(status_code=409, detail="CHARM_LIMIT")
    wallet.withdrawable_coins -= payload.amount
    wallet.charm_value -= required_charm
    wallet.frozen_coins += payload.amount
    return WithdrawResponse(status="reviewing", wallet=wallet)
