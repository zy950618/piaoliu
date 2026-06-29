import os
import sqlite3

from fastapi.testclient import TestClient

from app.main import app
from app import db_business


client = TestClient(app)
DEFAULT_USER_ID = "100000000001"
CREATOR_001_ID = "200000000001"
CREATOR_004_ID = "200000000004"


def admin_headers() -> dict[str, str]:
    response = client.post("/admin/auth/login", json={"username": "admin", "password": "admin_mock_password"})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_me_status_contains_quota_and_reward_state():
    response = client.get("/me/status")
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["id"].isdigit()
    assert "fish_bottle" in data["quotas"]
    assert data["ad_reward"]["reward_per_quota"] == 10
    assert data["checkin"]["week_rewards"] == [10, 10, 30, 10, 10, 30, 100]


def test_profile_update_persists_avatar_and_nickname():
    bottle = client.post(
        "/bottles",
        json={"content": "资料更新前发布的瓶子也要显示最新头像。"},
    )
    plaza = client.post(
        "/plaza/posts",
        json={"content": "资料更新前发布的广场动态也要显示最新头像。", "media_type": "text", "media_count": 0},
    )
    response = client.patch(
        "/me/profile",
        json={"nickname": "profile_contract_user", "avatar_text": "图", "avatar_url": "file://avatar_contract.png"},
    )
    status = client.get("/me/status")
    bottles = client.get("/bottles")
    plaza_detail = client.get(f"/plaza/posts/{plaza.json()['id']}")

    assert bottle.status_code == 200
    assert plaza.status_code == 200
    assert response.status_code == 200
    assert response.json()["nickname"] == "profile_contract_user"
    assert response.json()["avatar_text"] == "图"
    assert response.json()["avatar_url"] == "file://avatar_contract.png"
    assert status.json()["user"]["nickname"] == "profile_contract_user"
    assert status.json()["user"]["avatar_url"] == "file://avatar_contract.png"
    updated_bottle = next(item for item in bottles.json() if item["id"] == bottle.json()["id"])
    assert updated_bottle["author_name"] == "profile_contract_user"
    assert updated_bottle["author_avatar_text"] == "图"
    assert updated_bottle["author_avatar_url"] == "file://avatar_contract.png"
    assert plaza_detail.json()["author_name"] == "profile_contract_user"
    assert plaza_detail.json()["icon_text"] == "图"
    assert plaza_detail.json()["icon_url"] == "file://avatar_contract.png"


def test_profile_update_syncs_business_snapshots_and_game_turns():
    bottle = client.post("/bottles", json={"content": "profile sync bottle"})
    plaza = client.post("/plaza/posts", json={"content": "profile sync plaza", "media_type": "text", "media_count": 0})
    treehole = client.post("/treehole/posts", json={"content": "profile sync treehole"})
    comment = client.post(f"/plaza/posts/{plaza.json()['id']}/comments", json={"content": "profile sync comment"})
    thread_id = client.get("/conversations").json()[0]["id"]
    turn = client.post(f"/conversations/{thread_id}/turns", json={"body": "profile sync turn", "type": "text"})

    response = client.patch(
        "/me/profile",
        json={"nickname": "profile_sync_user", "avatar_text": "S", "avatar_url": "file://profile_sync.png"},
    )
    room = client.post(f"/conversations/{thread_id}/rooms", json={"mode": "truth"})
    gift = client.post(f"/conversations/{thread_id}/gifts", json={"gift_id": "gift_shell"})

    assert bottle.status_code == 200
    assert plaza.status_code == 200
    assert treehole.status_code == 200
    assert comment.status_code == 200
    assert turn.status_code == 200
    assert response.status_code == 200
    assert room.status_code == 200
    assert gift.status_code == 200
    assert room.json()["thread"]["turns"][-1]["sender_name"] == "profile_sync_user"
    assert gift.json()["thread"]["turns"][-1]["sender_name"] == "profile_sync_user"

    with sqlite3.connect(os.environ["PLAZA_SQLITE_PATH"]) as conn:
        assert conn.execute("select author_name from bottles where id = ?", (bottle.json()["id"],)).fetchone()[0] == "profile_sync_user"
        assert conn.execute("select author_name from plaza_posts where id = ?", (plaza.json()["id"],)).fetchone()[0] == "profile_sync_user"
        assert conn.execute("select author_name from treehole_posts where id = ?", (treehole.json()["id"],)).fetchone()[0] == "profile_sync_user"
        assert conn.execute(
            "select author_name from plaza_comments where post_id = ? and content = ?",
            (plaza.json()["id"], "profile sync comment"),
        ).fetchone()[0] == "profile_sync_user"
        assert conn.execute("select sender_name from conversation_turns where id = ?", (turn.json()["turns"][-1]["id"],)).fetchone()[0] == "profile_sync_user"


def test_client_id_creates_distinct_user_accounts():
    user_a_headers = {"X-Client-Id": "user_contract_alpha"}
    user_b_headers = {"X-Client-Id": "user_contract_beta"}

    user_a = client.get("/me/status", headers=user_a_headers)
    user_b = client.get("/me/status", headers=user_b_headers)
    renamed_a = client.patch(
        "/me/profile",
        json={"nickname": "alpha_user", "avatar_text": "甲", "avatar_url": "file://alpha.png"},
        headers=user_a_headers,
    )
    user_a_after = client.get("/me/status", headers=user_a_headers)
    user_b_after = client.get("/me/status", headers=user_b_headers)

    assert user_a.status_code == 200
    assert user_b.status_code == 200
    assert user_a.json()["user"]["id"].isdigit()
    assert user_b.json()["user"]["id"].isdigit()
    assert user_a.json()["user"]["id"] != user_b.json()["user"]["id"]
    assert user_a.json()["user"]["id"] == user_a_after.json()["user"]["id"]
    assert renamed_a.status_code == 200
    assert user_a_after.json()["user"]["nickname"] == "alpha_user"
    assert user_a_after.json()["user"]["avatar_url"] == "file://alpha.png"
    assert user_b_after.json()["user"]["nickname"] != "alpha_user"
    assert user_b_after.json()["user"]["avatar_url"] != "file://alpha.png"


def test_user_records_are_database_backed():
    before = client.get("/me/records")
    truth_before = next(item for item in before.json() if item["type"] == "truth")["count"]
    game_before = next(item for item in before.json() if item["type"] == "game")["count"]

    saved_truth = client.post(
        "/me/records",
        json={
            "record_type": "truth",
            "title": "私密真心话",
            "content": "记录接口契约测试",
            "visibility": "private",
            "source_type": "truth",
            "source_id": "truth_contract_001",
        },
    )
    saved_game = client.post(
        "/me/records",
        json={
            "record_type": "game",
            "title": "常规真心话",
            "content": "游戏记录接口契约测试",
            "visibility": "private",
            "source_type": "truth_public",
        },
    )
    after = client.get("/me/records")
    truth_after = next(item for item in after.json() if item["type"] == "truth")["count"]
    game_after = next(item for item in after.json() if item["type"] == "game")["count"]

    assert before.status_code == 200
    assert saved_truth.status_code == 200
    assert saved_truth.json()["record_type"] == "truth"
    assert saved_game.status_code == 200
    assert after.status_code == 200
    assert truth_after == truth_before + 1
    assert game_after == game_before + 1


def test_prompt_and_membership_configs_are_database_backed():
    truth = client.get("/truth/questions")
    dare = client.get("/dare/tasks")
    game_prompt = client.get("/game/prompts/random", params={"mode": "truth_public"})
    products = client.get("/membership/products")

    assert truth.status_code == 200
    assert dare.status_code == 200
    assert game_prompt.status_code == 200
    assert products.status_code == 200
    assert game_prompt.json()["mode"] == "truth_public"
    assert products.json()[0]["price_label"].startswith("¥")

    with sqlite3.connect(os.environ["PLAZA_SQLITE_PATH"]) as conn:
        prompt_count = conn.execute("select count(*) from prompt_templates").fetchone()[0]
        product_count = conn.execute("select count(*) from membership_product_configs").fetchone()[0]

    assert prompt_count >= 18
    assert product_count >= 3


def test_ad_reward_commit_is_idempotent():
    prepared = client.post("/ads/reward/prepare").json()
    first = client.post(
        "/ads/reward/commit",
        json={"reward_session_id": prepared["reward_session_id"], "completed": True},
    )
    second = client.post(
        "/ads/reward/commit",
        json={"reward_session_id": prepared["reward_session_id"], "completed": True},
    )
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["quotas"]["fish_bottle"]["remaining"] == second.json()["quotas"]["fish_bottle"]["remaining"]


def test_quota_consume_business_id_is_idempotent():
    payload = {"quota_type": "truth", "business_id": "truth:test_case_001"}
    first = client.post("/quota/consume", json=payload)
    second = client.post("/quota/consume", json=payload)
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["remaining"] == second.json()["remaining"]


def test_wallet_separates_recharge_and_withdrawable_coins():
    response = client.get("/wallet")
    assert response.status_code == 200
    data = response.json()["wallet"]
    assert data["recharge_coins"] > 0
    assert data["withdrawable_coins"] <= data["earned_coins"]
    assert data["charm_value"] >= data["withdraw_threshold_charm"]


def test_private_photo_unlock_spends_recharge_coin_only():
    before = client.get("/wallet").json()["wallet"]["recharge_coins"]
    response = client.post("/private-photos/unlock", json={"photo_id": "photo_001"})
    assert response.status_code == 200
    after = response.json()["wallet"]["recharge_coins"]
    assert after < before


def test_verification_and_nearby_contracts_exist():
    verification = client.get("/verification")
    nearby = client.get("/nearby/users")
    plaza = client.get("/plaza/posts")
    assert verification.status_code == 200
    assert verification.json()["verification"]["gender_verified"] is True
    assert nearby.status_code == 200
    assert plaza.status_code == 200
    media_post = next(item for item in plaza.json() if item["media"])
    assert "view_count" in media_post
    assert "media_type" in media_post
    assert "media" in media_post
    assert media_post["media"][0]["owner_id"] == media_post["author_id"]
    assert media_post["media"][0]["url"].startswith("https://")
    assert {item["media_type"] for post in plaza.json() for item in post["media"]} >= {"image", "voice", "video"}


def test_seed_referral_invite_code_collision_does_not_break_new_user():
    target_user_id = "900000000009"
    conflicting_user_id = "900000000010"
    invite_code = db_business.invite_code_for_user(target_user_id)
    created_at = "2026-01-01T00:00:00+00:00"

    with sqlite3.connect(os.environ["PLAZA_SQLITE_PATH"]) as conn:
        conn.execute("delete from referral_accounts where user_id in (?, ?) or invite_code = ?", (target_user_id, conflicting_user_id, invite_code))
        conn.execute(
            """
            insert or ignore into users (
              id, nickname, role, avatar_text, platform, gender, is_vip, vip_level,
              drift_coins, face_verified, gender_verified, charm_value, status, created_at
            ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (conflicting_user_id, "invite_collision_owner", "user", "I", "h5", "unknown", 0, "none", 0, 0, 0, 0, "active", created_at),
        )
        conn.execute(
            "insert into referral_accounts (user_id, invite_code, invited_count, reward_vip_days, next_reward_need) values (?, ?, ?, ?, ?)",
            (conflicting_user_id, invite_code, 0, 0, 5),
        )
        conn.commit()

    response = client.get("/verification", headers={"X-Client-Id": target_user_id})
    assert response.status_code == 200
    assert response.json()["referral"]["invite_code"].startswith("SEA")
    assert response.json()["referral"]["invite_code"] != invite_code


def test_verification_submission_is_review_gated():
    headers = admin_headers()
    rejected = client.post(
        f"/admin/verification/{DEFAULT_USER_ID}/review",
        json={"action": "reject", "reason": "contract_reset"},
        headers=headers,
    )
    submitted = client.post("/verification/face")
    pending_status = client.get("/me/status")
    approved = client.post(
        f"/admin/verification/{DEFAULT_USER_ID}/review",
        json={"action": "approve", "reason": "contract_restore"},
        headers=headers,
    )

    assert rejected.status_code == 200
    assert submitted.status_code == 200
    assert submitted.json()["manual_review_status"] == "pending"
    assert pending_status.json()["user"]["face_verified"] is False
    assert approved.status_code == 200
    assert approved.json()["manual_review_status"] == "approved"
    assert client.get("/me/status").json()["user"]["face_verified"] is True


def test_plaza_publish_contract():
    plain = client.post(
        "/plaza/posts",
        json={"content": "今天只发布一条纯文字动态。"},
    )
    assert plain.status_code == 200
    assert plain.json()["media_type"] == "text"
    assert plain.json()["media_count"] == 0
    assert plain.json()["media"] == []

    response = client.post(
        "/plaza/posts",
        json={"content": "今天在广场发一条图文动态。", "media_type": "image", "media_count": 2},
    )
    posts = client.get("/plaza/posts")

    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "今天在广场发一条图文动态。"
    assert data["media_type"] == "image"
    assert data["media_count"] == 2
    assert data["media"]
    assert data["media"][0]["post_id"] == data["id"]
    assert data["media"][0]["owner_id"] == data["author_id"]
    assert data["view_count"] == 0
    assert posts.json()[0]["id"] == data["id"]

    video = client.post(
        "/plaza/posts",
        json={"content": "今天在广场发一条视频动态。", "media_type": "video", "media_count": 1},
    )
    assert video.status_code == 200
    assert video.json()["media_type"] == "video"


def test_plaza_filters_and_comments_contract():
    filtered = client.get("/plaza/posts", params={"city": "杭州", "gender": "男", "age_range": "24-31"})
    assert filtered.status_code == 200
    assert filtered.json()
    assert all(item["city"] == "杭州" and item["gender"] == "male" and item["age_range"] == "25-30" for item in filtered.json())

    post_id = filtered.json()[0]["id"]
    commented = client.post(f"/plaza/posts/{post_id}/comments", json={"content": "这条动态我也有同感。"})
    assert commented.status_code == 200
    assert commented.json()["comment_preview"] == "这条动态我也有同感。"
    assert commented.json()["comment_count"] >= filtered.json()[0]["comment_count"] + 1
    comments = client.get(f"/plaza/posts/{post_id}/comments")
    assert comments.status_code == 200
    assert any(item["content"] == "这条动态我也有同感。" for item in comments.json())
    assert {"author_gender", "author_age_range", "author_verified", "author_city"} <= set(comments.json()[0])

    liked = client.post(f"/plaza/posts/{post_id}/like")
    assert liked.status_code == 200
    assert liked.json()["like_count"] >= filtered.json()[0]["like_count"] + 1


def test_plaza_interactions_are_persisted_to_local_db():
    first_list = client.get("/plaza/posts")
    second_list = client.get("/plaza/posts")
    assert first_list.status_code == 200
    assert second_list.status_code == 200

    post_id = first_list.json()[0]["id"]
    first_view_count = first_list.json()[0]["view_count"]
    second_post = next(item for item in second_list.json() if item["id"] == post_id)
    assert second_post["view_count"] == first_view_count + 1

    liked = client.post(f"/plaza/posts/{post_id}/like")
    commented = client.post(f"/plaza/posts/{post_id}/comments", json={"content": "数据库持久化留言"})
    assert liked.status_code == 200
    assert commented.status_code == 200

    with sqlite3.connect(os.environ["PLAZA_SQLITE_PATH"]) as conn:
        like_count = conn.execute("select count(*) from plaza_likes where post_id = ?", (post_id,)).fetchone()[0]
        comment_count = conn.execute(
            "select count(*) from plaza_comments where post_id = ? and content = ?",
            (post_id, "数据库持久化留言"),
        ).fetchone()[0]
        view_count = conn.execute("select view_count from plaza_posts where id = ?", (post_id,)).fetchone()[0]

    assert like_count >= 1
    assert comment_count == 1
    assert view_count >= 2


def test_plaza_like_toggles_for_current_user():
    created = client.post("/plaza/posts", json={"content": "点赞切换契约测试", "media_type": "text", "media_count": 0})
    assert created.status_code == 200
    post_id = created.json()["id"]

    liked = client.post(f"/plaza/posts/{post_id}/like")
    unliked = client.post(f"/plaza/posts/{post_id}/like")
    assert liked.status_code == 200
    assert unliked.status_code == 200
    assert liked.json()["like_count"] == created.json()["like_count"] + 1
    assert liked.json()["liked_by_current_user"] is True
    assert unliked.json()["like_count"] == created.json()["like_count"]
    assert unliked.json()["liked_by_current_user"] is False

    with sqlite3.connect(os.environ["PLAZA_SQLITE_PATH"]) as conn:
        like_rows = conn.execute(
            "select count(*) from plaza_likes where post_id = ? and user_id = ?",
            (post_id, DEFAULT_USER_ID),
        ).fetchone()[0]
    assert like_rows == 0


def test_plaza_hidden_comments_visibility_contract():
    post_id = "plaza_001"
    post_detail = client.get(f"/plaza/posts/{post_id}")
    default_comments = client.get(f"/plaza/posts/{post_id}/comments")
    owner_comments = client.get(f"/plaza/posts/{post_id}/comments", params={"viewer_id": CREATOR_001_ID})
    hidden = client.post(
        f"/plaza/posts/{post_id}/comments",
        json={"content": "这条留言只给发布者看。", "hidden_for_owner_only": True},
    )
    commenter_comments = client.get(f"/plaza/posts/{post_id}/comments", params={"viewer_id": DEFAULT_USER_ID})
    owner_comments_after = client.get(f"/plaza/posts/{post_id}/comments", params={"viewer_id": CREATOR_001_ID})

    assert post_detail.status_code == 200
    assert post_detail.json()["id"] == post_id
    assert post_detail.json()["author_id"] == CREATOR_001_ID
    assert default_comments.status_code == 200
    assert all(item["content"] != "这条只想给发布者看到。" for item in default_comments.json())
    assert owner_comments.status_code == 200
    seeded_hidden = next(item for item in owner_comments.json() if item["content"] == "这条只想给发布者看到。")
    assert seeded_hidden["author_name"] == "匿名留言"
    assert seeded_hidden["icon_text"] == "匿"
    assert seeded_hidden["author_gender"] == "unknown"
    assert seeded_hidden["author_age_range"] is None
    assert seeded_hidden["author_city"] is None
    assert hidden.status_code == 200
    assert hidden.json()["comment_preview"] != "这条留言只给发布者看。"
    assert all(item["content"] != "这条留言只给发布者看。" for item in commenter_comments.json())
    created_hidden = next(item for item in owner_comments_after.json() if item["content"] == "这条留言只给发布者看。")
    assert created_hidden["hidden_for_owner_only"] is True
    assert created_hidden["author_name"] == "匿名留言"
    assert created_hidden["icon_text"] == "匿"
    assert created_hidden["author_id"] == "anonymous"


def test_nearby_users_filters_contract():
    filtered = client.get("/nearby/users", params={"gender": "女", "age_range": "25-30", "distance_km": 3})
    assert filtered.status_code == 200
    assert filtered.json()
    assert all(item["gender"] == "female" and item["age_range"] == "25-30" and item["distance_km"] <= 3 for item in filtered.json())


def test_checkin_is_idempotent_for_today():
    first = client.post("/checkin")
    second = client.post("/checkin")
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["checked_today"] is True
    assert second.json()["checked_today"] is True
    assert first.json()["streak_days"] == second.json()["streak_days"]
    assert first.json()["last_reward"] == second.json()["last_reward"]


def test_membership_order_verify_is_idempotent_by_transaction():
    payload = {
        "platform": "wechat",
        "product_id": "vip_season",
        "transaction_id": "txn_contract_001",
        "receipt": "mock_receipt",
    }
    first = client.post("/membership/orders/verify", json=payload)
    second = client.post("/membership/orders/verify", json=payload)
    orders = client.get("/membership/orders")
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["order"]["id"] == second.json()["order"]["id"]
    assert second.json()["order"]["status"] == "duplicate_verified"
    assert orders.status_code == 200
    assert any(item["transaction_id"] == "txn_contract_001" for item in orders.json())


def test_reports_and_blocks_are_idempotent():
    report_payload = {"target_type": "bottle", "target_id": "bottle_001", "reason": "spam"}
    first_report = client.post("/reports", json=report_payload)
    second_report = client.post("/reports", json=report_payload)
    first_block = client.post("/blocks", json={"blocked_user_id": "bad_user_contract"})
    second_block = client.post("/blocks", json={"blocked_user_id": "bad_user_contract"})
    assert first_report.status_code == 200
    assert second_report.status_code == 200
    assert first_report.json()["id"] == second_report.json()["id"]
    assert first_block.status_code == 200
    assert second_block.status_code == 200
    assert first_block.json()["id"] == second_block.json()["id"]


def test_chat_moderation_and_flash_view_are_backend_controlled():
    thread_id = client.get("/conversations").json()[0]["id"]
    risky = client.post(
        f"/conversations/{thread_id}/turns",
        json={"body": "hello wx telegram", "type": "text"},
    )
    flash = client.post(
        f"/conversations/{thread_id}/turns",
        json={"body": "flash image contract", "type": "flash_image", "media_url": "file://flash.png"},
    )
    turn_id = flash.json()["turns"][-1]["id"]
    viewed = client.post(f"/conversations/{thread_id}/turns/{turn_id}/view")
    reports = client.get("/reports")

    assert risky.status_code == 200
    assert risky.json()["last_message"] == "hello ** ********"
    assert reports.status_code == 200
    assert any(item["target_type"] == "chat" and item["target_id"] == thread_id and item["status"] == "reviewing" for item in reports.json())
    assert flash.status_code == 200
    assert flash.json()["turns"][-1]["flash_viewed"] is False
    assert viewed.status_code == 200
    assert viewed.json()["turns"][-1]["flash_viewed"] is True


def test_conversations_are_user_scoped_and_admin_chats_are_monitored():
    headers = admin_headers()
    conversations = client.get("/conversations")
    chats = client.get("/admin/chats", headers=headers)

    assert conversations.status_code == 200
    thread = conversations.json()[0]
    assert thread["participant_user_id"]
    assert "participant_avatar_text" in thread
    assert "turns" in thread

    assert chats.status_code == 200
    chat = next(item for item in chats.json() if item["thread_id"] == thread["id"])
    assert thread["participant_user_id"] in chat["participant_user_ids"]
    assert chat["participants"]
    assert chat["messages"]


def test_treehole_react_is_idempotent_for_same_post():
    post_id = client.get("/treehole/feed").json()[0]["id"]
    first = client.post(f"/treehole/{post_id}/react")
    second = client.post(f"/treehole/{post_id}/react")
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["post"]["resonance_count"] == second.json()["post"]["resonance_count"]


def test_admin_business_skeleton_contracts_exist():
    headers = admin_headers()
    moderation = client.post(
        "/admin/moderation/job_contract_001",
        json={"action": "reject", "reason": "policy"},
        headers=headers,
    )
    audit = client.get("/admin/audit")
    wallet = client.get("/admin/wallet")
    verification = client.get("/admin/verification")
    referral = client.get("/admin/referral")
    nearby = client.get("/admin/nearby")
    plaza = client.get("/admin/plaza")
    content = client.get("/admin/content")
    users = client.get("/admin/users")

    assert moderation.status_code == 200
    assert moderation.json()["action"] == "reject"
    assert audit.status_code == 200
    assert any(item["target_id"] == "job_contract_001" for item in audit.json())
    assert wallet.status_code == 200
    assert "pending_withdrawals" in wallet.json()
    assert verification.status_code == 200
    assert referral.status_code == 200
    assert nearby.status_code == 200
    assert plaza.status_code == 200
    assert content.status_code == 200
    assert users.status_code == 200


def test_collection_skeletons_are_available():
    assert client.get("/users/me/status").status_code == 200
    assert client.get("/bottles").status_code == 200
    assert client.get("/truth/questions").status_code == 200
    assert client.get("/dare/tasks").status_code == 200


def test_bottle_pool_has_seeded_author_details_and_random_rotation():
    bottles = client.get("/bottles")
    assert bottles.status_code == 200
    data = bottles.json()
    assert len(data) >= 8
    assert len({item["author_id"] for item in data}) >= 8
    assert any(item["author_gender"] == "female" and item["author_verified"] is True for item in data)
    assert any(item["author_gender"] == "male" for item in data)
    assert any(item["author_vip"] is True for item in data)

    first = client.get("/bottles/random")
    second = client.get("/bottles/random")
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["author_id"] != second.json()["author_id"]


def test_follow_state_is_reflected_in_backend_bottle_data():
    target_user_id = CREATOR_004_ID
    follow = client.post("/relations/follow", json={"target_user_id": target_user_id})
    bottles = client.get("/bottles")

    assert follow.status_code == 200
    assert any(item["author_id"] == target_user_id and item["is_following"] is True for item in bottles.json())


def test_random_bottle_respects_filter_query_params():
    response = client.get("/bottles/random", params={"city": "同城", "gender": "女", "age_range": "18-24"})
    assert response.status_code == 200
    data = response.json()
    assert data["author_city"] == "杭州"
    assert data["author_gender"] == "female"
    assert data["author_age_range"] == "18-24"


def test_random_bottle_no_match_does_not_consume_quota():
    before = client.get("/quota/today").json()["fish_bottle"]["remaining"]
    response = client.get("/bottles/random", params={"city": "同城", "gender": "女", "age_range": "37+"})
    after = client.get("/quota/today").json()["fish_bottle"]["remaining"]

    assert response.status_code == 404
    assert after == before


def test_create_bottle_uses_target_scope_not_manual_city():
    response = client.post(
        "/bottles",
        json={
            "content": "今晚把这句话交给同城的人。",
            "target_gender": "female",
            "target_scope": "same_city",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["author_city"] == "杭州"
    assert data["target_gender"] == "female"
    assert data["target_scope"] == "same_city"
    assert "target_city" not in data


def test_random_bottle_prompt_contract():
    response = client.get("/bottles/prompts/random")
    assert response.status_code == 200
    assert response.json()["content"].strip()


def test_empty_bottle_content_does_not_consume_throw_quota():
    before = client.get("/quota/today").json()["throw_bottle"]["remaining"]
    response = client.post("/bottles", json={"content": "   "})
    after = client.get("/quota/today").json()["throw_bottle"]["remaining"]

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "EMPTY_BOTTLE_CONTENT"
    assert after == before


def test_admin_auth_login_me_logout_and_write_audit():
    headers = admin_headers()

    me = client.get("/admin/auth/me", headers=headers)
    logout = client.post("/admin/auth/logout", headers=headers)
    reward_config = client.get("/admin/reward-config").json()
    update = client.patch("/admin/reward-config", json=reward_config, headers=headers)
    audit = client.get("/admin/audit")

    assert me.status_code == 200
    assert me.json()["roles"] == ["admin", "moderator"]
    assert logout.status_code == 200
    assert logout.json()["status"] == "logged_out"
    assert update.status_code == 200
    assert any(item["action"] == "update_reward_config" for item in audit.json())


def test_admin_write_requires_mock_token_with_unified_error():
    response = client.post("/admin/moderation/job_auth_required", json={"action": "reject"})

    assert response.status_code == 401
    assert response.json() == {
        "error": {
            "code": "ADMIN_UNAUTHORIZED",
            "message": "Admin bearer token is required",
        }
    }


def test_blocked_user_is_rejected_from_user_scope():
    headers = admin_headers()
    try:
        blocked = client.post(f"/admin/users/{DEFAULT_USER_ID}/status", json={"status": "blocked"}, headers=headers)
        denied = client.get("/me/status")

        assert blocked.status_code == 200
        assert blocked.json()["status"] == "blocked"
        assert denied.status_code == 403
        assert denied.json()["error"]["code"] == "USER_BLOCKED"
    finally:
        recover = client.post(f"/admin/users/{DEFAULT_USER_ID}/status", json={"status": "active"}, headers=headers)
        assert recover.status_code == 200


def test_backend_infrastructure_placeholders_import_without_connections():
    from app import db
    from app.models import AdminAuditLog, Base, Bottle, BottleReply, Follow, PlazaComment, PlazaLike, PlazaMedia, PlazaPost, User
    from app.redis import get_redis_client
    from app.settings import get_settings

    settings = get_settings()
    redis_client = get_redis_client()

    assert settings.database_url.startswith(("postgresql+asyncpg://", "sqlite+aiosqlite:///"))
    assert db.engine.url.drivername in {"postgresql+asyncpg", "sqlite+aiosqlite"}
    assert User.__tablename__ in Base.metadata.tables
    assert AdminAuditLog.__tablename__ in Base.metadata.tables
    assert Bottle.__tablename__ in Base.metadata.tables
    assert BottleReply.__tablename__ in Base.metadata.tables
    assert Follow.__tablename__ in Base.metadata.tables
    assert PlazaPost.__tablename__ in Base.metadata.tables
    assert PlazaMedia.__tablename__ in Base.metadata.tables
    assert PlazaComment.__tablename__ in Base.metadata.tables
    assert PlazaLike.__tablename__ in Base.metadata.tables
    assert redis_client.connection_pool.connection_kwargs["host"] == "localhost"
