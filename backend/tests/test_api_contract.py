import os
import sqlite3

from fastapi.testclient import TestClient

from app.main import app
from app import chat_store, db_business


client = TestClient(app)
DEFAULT_USER_ID = "100000000001"
CREATOR_001_ID = "200000000001"
CREATOR_002_ID = "200000000002"
CREATOR_003_ID = "200000000003"
CREATOR_004_ID = "200000000004"
CREATOR_006_ID = "200000000006"


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


def test_game_random_match_uses_game_quota_and_filters():
    before = client.get("/quota/today").json()["truth"]["remaining"]
    payload = {
        "mode": "truth",
        "gender": "female",
        "age_range": "25-30",
        "client_match_id": "contract_match_001",
    }
    first = client.post("/game/random-match", json=payload)
    second = client.post("/game/random-match", json=payload)
    after = client.get("/quota/today").json()["truth"]["remaining"]

    assert first.status_code == 200
    data = first.json()
    assert data["status"] == "matched"
    assert data["mode"] == "truth"
    assert data["source_type"] == "game_room"
    assert data["source_id"] == data["room_id"]
    assert data["evidence_id"] == f"game_random_match:{data['room_id']}"
    assert data["next_action"] == "wait_confirm"
    assert data["target_user"]["gender"] == "female"
    assert data["target_user"]["age_range"] == "25-30"
    assert data["quota"]["type"] == "truth"
    assert data["quota"]["remaining"] == before - 1
    assert second.status_code == 200
    assert second.json()["quota"]["remaining"] == before - 1
    assert after == before - 1


def test_game_random_match_no_match_does_not_consume_quota():
    before = client.get("/quota/today").json()["dare"]["remaining"]
    response = client.post(
        "/game/random-match",
        json={
            "mode": "dare",
            "gender": "female",
            "age_range": "77-88",
            "client_match_id": "contract_match_no_result",
        },
    )
    after = client.get("/quota/today").json()["dare"]["remaining"]

    assert response.status_code == 404
    assert after == before


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


def test_private_photo_low_risk_ai_auto_approved_and_unlockable():
    uploaded = client.post(
        "/private-photos",
        json={
            "file_id": "safe_low_contract_001",
            "caption": "safe daily photo",
            "client_upload_id": "upload_low_contract_001",
        },
    )
    photo_id = uploaded.json()["id"]
    detail = client.get(f"/private-photos/{photo_id}")
    unlocked = client.post(f"/private-photos/{photo_id}/unlock")

    assert uploaded.status_code == 200
    assert uploaded.json()["review_status"] == "ai_approved"
    assert uploaded.json()["risk_level"] == "low_risk"
    assert uploaded.json()["revenue_state"] == "eligible"
    assert "non_explicit" in uploaded.json()["model_labels"]
    assert detail.status_code == 200
    assert detail.json()["id"] == photo_id
    assert unlocked.status_code == 200
    assert unlocked.json()["creator_revenue_state"] == "eligible"
    assert unlocked.json()["audit_id"].startswith("audit_")


def test_private_photo_medium_risk_requires_manual_review_then_can_release_revenue():
    headers = admin_headers()
    uploaded = client.post(
        "/private-photos",
        json={
            "file_id": "manual_borderline_contract_001",
            "caption": "manual borderline low_confidence",
            "client_upload_id": "upload_manual_contract_001",
        },
    )
    photo_id = uploaded.json()["id"]
    pending_unlock = client.post(f"/private-photos/{photo_id}/unlock")
    reviewed = client.post(
        f"/admin/private-photos/reviews/{photo_id}/review",
        json={
            "action": "approve",
            "reason": "人工复核通过",
            "manual_labels": ["manual_safe"],
            "revenue_action": "release",
        },
        headers=headers,
    )
    unlocked = client.post(f"/private-photos/{photo_id}/unlock")

    assert uploaded.status_code == 200
    assert uploaded.json()["review_status"] == "manual_required"
    assert uploaded.json()["risk_level"] == "medium_risk"
    assert uploaded.json()["revenue_state"] == "frozen"
    assert pending_unlock.status_code == 409
    assert pending_unlock.json()["error"]["code"] == "PHOTO_REVIEW_PENDING"
    assert reviewed.status_code == 200
    assert reviewed.json()["before_status"] == "manual_required"
    assert reviewed.json()["after_status"] == "manual_approved"
    assert reviewed.json()["after_revenue_state"] == "eligible"
    assert unlocked.status_code == 200
    assert unlocked.json()["creator_revenue_state"] == "eligible"


def test_private_photo_high_risk_frozen_and_not_unlockable():
    uploaded = client.post(
        "/private-photos",
        json={
            "file_id": "minor_fraud_high_contract_001",
            "caption": "minor fraud high",
            "client_upload_id": "upload_high_contract_001",
        },
    )
    photo_id = uploaded.json()["id"]
    unlocked = client.post(f"/private-photos/{photo_id}/unlock")

    assert uploaded.status_code == 200
    assert uploaded.json()["review_status"] == "frozen"
    assert uploaded.json()["risk_level"] == "high_risk"
    assert uploaded.json()["revenue_state"] == "ineligible"
    assert unlocked.status_code == 409
    assert unlocked.json()["error"]["code"] == "PHOTO_FROZEN"


def test_private_photo_frozen_asset_can_be_appealed_and_persists():
    uploaded = client.post(
        "/private-photos",
        json={
            "file_id": "minor_fraud_high_contract_appeal",
            "caption": "minor fraud high appeal",
            "client_upload_id": "upload_high_contract_appeal",
        },
    )
    photo_id = uploaded.json()["id"]
    appealed = client.post(
        f"/private-photos/{photo_id}/appeal",
        json={"reason": "误判申诉，要求人工复核"},
    )
    detail = client.get(f"/private-photos/{photo_id}")
    pending_unlock = client.post(f"/private-photos/{photo_id}/unlock")

    assert uploaded.status_code == 200
    assert uploaded.json()["review_status"] == "frozen"
    assert appealed.status_code == 200
    assert appealed.json()["review_status"] == "appeal_pending"
    assert appealed.json()["revenue_state"] == "frozen"
    assert appealed.json()["audit_id"].startswith("audit_")
    audit_id = appealed.json()["audit_id"]
    assert detail.status_code == 200
    assert detail.json()["appeal_state"].startswith("pending:")
    assert audit_id in detail.json()["audit_refs"]
    assert pending_unlock.status_code == 409
    assert pending_unlock.json()["error"]["code"] == "PHOTO_REVIEW_PENDING"

    with sqlite3.connect(os.environ["PLAZA_SQLITE_PATH"]) as conn:
        persisted = conn.execute(
            "select status, revenue_state, appeal_state from private_photo_assets where id = ?",
            (photo_id,),
        ).fetchone()
        audit_persisted = conn.execute(
            "select action, target_id from admin_audit_logs where id = ?",
            (audit_id,),
        ).fetchone()
    assert audit_persisted == ("private_photo_appeal", photo_id)
    assert persisted == ("appeal_pending", "frozen", "pending:误判申诉，要求人工复核")


def test_validation_error_includes_field_codes():
    response = client.post("/private-photos/photo_missing/appeal", json={"reason": ""})

    assert response.status_code == 422
    payload = response.json()["error"]
    assert payload["code"] == "VALIDATION_ERROR"
    field_errors = payload["details"]["field_errors"]
    assert field_errors[0]["field"] == "body.reason"
    assert field_errors[0]["code"] == "FIELD_TOO_SHORT"
    assert payload["details"]["raw_errors"]


def test_admin_private_photo_reviews_filter_and_risk_summary():
    headers = admin_headers()
    client.post(
        "/private-photos",
        json={
            "file_id": "safe_low_contract_002",
            "caption": "safe second photo",
            "client_upload_id": "upload_low_contract_002",
        },
    )
    client.post(
        "/private-photos",
        json={
            "file_id": "manual_contract_002",
            "caption": "manual borderline",
            "client_upload_id": "upload_manual_contract_002",
        },
    )
    reviews = client.get("/admin/private-photos/reviews", params={"risk_level": "medium_risk"}, headers=headers)
    summary = client.get("/admin/private-photos/risk-summary", headers=headers)

    assert reviews.status_code == 200
    assert reviews.json()
    assert all(item["risk_level"] == "medium_risk" for item in reviews.json())
    assert summary.status_code == 200
    assert summary.json()["low_risk"] >= 1
    assert summary.json()["medium_risk"] >= 1
    assert "manual_required" in summary.json()


def test_verification_and_nearby_contracts_exist():
    verification = client.get("/verification")
    nearby = client.get("/nearby/users")
    plaza = client.get("/plaza/posts")
    assert verification.status_code == 200
    assert verification.json()["verification"]["gender_verified"] is True
    assert nearby.status_code == 200
    assert nearby.json()[0]["icon_url"].startswith("https://api.dicebear.com/9.x/open-peeps/svg")
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
    filtered = client.get("/nearby/users", params={"city": "杭州", "gender": "女", "age_range": "24-31"})
    assert filtered.status_code == 200
    assert filtered.json()
    assert all(item["city"] == "杭州" and item["gender"] == "female" for item in filtered.json())
    assert {item["age_range"] for item in filtered.json()} <= {"18-24", "25-30"}
    assert all(item["icon_url"].startswith("https://api.dicebear.com/9.x/open-peeps/svg") for item in filtered.json())


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


def test_context_chat_requires_interaction_source():
    response = client.post(
        "/chat/context-requests",
        json={
            "target_user_id": CREATOR_001_ID,
            "source_type": "bottle_reply",
            "initiator_action": "continue_chat",
        },
    )

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "CHAT_CONTEXT_REQUIRED"


def test_context_chat_bottle_reply_accept_creates_active_conversation():
    target_headers = {"X-User-Id": CREATOR_001_ID}
    created = client.post(
        "/chat/context-requests",
        json={
            "target_user_id": CREATOR_001_ID,
            "source_type": "bottle_reply",
            "source_id": "bottle_001",
            "reply_id": "reply_contract_001",
            "initiator_action": "continue_chat",
            "evidence_id": "reply_contract_001",
        },
    )
    accepted = client.post(
        f"/chat/context-requests/{created.json()['id']}/accept",
        json={"confirm_action": "reply", "evidence_id": "author_reply_contract_001"},
        headers=target_headers,
    )
    conversation_id = accepted.json()["conversation_id"]
    listed = client.get("/chat/conversations")
    detail = client.get(f"/chat/conversations/{conversation_id}")
    sent = client.post(
        f"/chat/conversations/{conversation_id}/messages",
        json={"content_type": "text", "content": "基于这次瓶子回应继续聊。", "client_message_id": "msg_context_contract_001"},
    )

    assert created.status_code == 200
    assert created.json()["status"] == "pending"
    assert created.json()["source_type"] == "bottle_reply"
    assert accepted.status_code == 200
    assert accepted.json()["status"] == "active"
    assert listed.status_code == 200
    assert any(item["id"] == conversation_id and item["status"] == "active" for item in listed.json())
    assert detail.status_code == 200
    assert detail.json()["source_id"] == "bottle_001"
    assert detail.json()["source_summary"]["title"] == "基于本次互动开启"
    assert sent.status_code == 200
    assert sent.json()["status"] == "sent"
    assert sent.json()["audit_id"].startswith("audit_")


def test_message_invitation_card_accept_reject_and_second_open_contract():
    invitation_headers = {"X-Client-Id": "loop20_invitation_user"}
    listed = client.get("/chat/context-requests", headers=invitation_headers)
    pending = next(item for item in listed.json() if item["status"] == "pending" and item["source_type"] == "game_room")
    accepted = client.post(
        f"/chat/context-requests/{pending['id']}/accept",
        json={"confirm_action": "room_confirm", "evidence_id": f"message_invite_accept:{pending['id']}"},
        headers=invitation_headers,
    )
    second_list = client.get("/chat/context-requests", headers=invitation_headers)
    active_card = next(item for item in second_list.json() if item["id"] == pending["id"])
    detail = client.get(f"/chat/conversations/{accepted.json()['conversation_id']}", headers=invitation_headers)

    reject_headers = {"X-Client-Id": "loop20_reject_user"}
    reject_list = client.get("/chat/context-requests", headers=reject_headers)
    reject_pending = next(item for item in reject_list.json() if item["status"] == "pending")
    rejected = client.post(
        f"/chat/context-requests/{reject_pending['id']}/reject",
        json={"reason": "user_cancel_from_messages"},
        headers=reject_headers,
    )

    assert listed.status_code == 200
    assert pending["source_summary"]["title"] == "游戏房间邀请"
    assert accepted.status_code == 200
    assert accepted.json()["status"] == "active"
    assert accepted.json()["conversation_id"]
    assert second_list.status_code == 200
    assert active_card["status"] == "active"
    assert active_card["conversation_id"] == accepted.json()["conversation_id"]
    assert detail.status_code == 200
    assert detail.json()["status"] == "active"
    assert detail.json()["source_type"] == "game_room"
    assert rejected.status_code == 200
    assert rejected.json()["status"] == "expired"


def test_context_conversation_survives_memory_store_reset():
    headers = {"X-Client-Id": "loop21_persist_user"}
    target_headers = {"X-User-Id": CREATOR_003_ID}
    created = client.post(
        "/chat/context-requests",
        json={
            "target_user_id": CREATOR_003_ID,
            "source_type": "plaza_comment",
            "source_id": "plaza_001:loop21_comment",
            "initiator_action": "continue_chat",
            "evidence_id": "loop21_comment_evidence",
        },
        headers=headers,
    )
    accepted = client.post(
        f"/chat/context-requests/{created.json()['id']}/accept",
        json={"confirm_action": "reply", "evidence_id": "loop21_accept"},
        headers=target_headers,
    )
    conversation_id = accepted.json()["conversation_id"]
    sent = client.post(
        f"/chat/conversations/{conversation_id}/messages",
        json={"content_type": "text", "content": "restart persistence message", "client_message_id": "msg_loop21_persist"},
        headers=headers,
    )

    chat_store.context_requests.clear()
    chat_store.conversations.clear()
    chat_store.blocked_pairs.clear()
    chat_store.reports.clear()

    detail = client.get(f"/chat/conversations/{conversation_id}", headers=headers)
    listed = client.get("/chat/conversations", headers=headers)

    assert created.status_code == 200
    assert accepted.status_code == 200
    assert sent.status_code == 200
    assert detail.status_code == 200
    assert detail.json()["id"] == conversation_id
    assert detail.json()["messages"][-1]["content"] == "restart persistence message"
    assert any(item["id"] == conversation_id for item in listed.json())


def test_context_chat_report_is_visible_to_admin_queue():
    headers = admin_headers()
    target_headers = {"X-User-Id": CREATOR_004_ID}
    created = client.post(
        "/chat/context-requests",
        json={
            "target_user_id": CREATOR_004_ID,
            "source_type": "plaza_comment",
            "source_id": "plaza_001:comment_contract_001",
            "initiator_action": "continue_chat",
            "evidence_id": "comment_contract_001",
        },
    )
    accepted = client.post(
        f"/chat/context-requests/{created.json()['id']}/accept",
        json={"confirm_action": "reply", "evidence_id": "plaza_author_reply_contract_001"},
        headers=target_headers,
    )
    conversation_id = accepted.json()["conversation_id"]
    reported = client.post(
        f"/chat/conversations/{conversation_id}/report",
        json={"reason": "harassment", "message_ids": [], "description": "contract report"},
    )
    admin_detail = client.get(f"/admin/chat/conversations/{conversation_id}", headers=headers)
    admin_requests = client.get("/admin/chat/context-requests", headers=headers)

    assert reported.status_code == 200
    assert reported.json()["conversation_status"] == "reported"
    assert admin_detail.status_code == 200
    assert admin_detail.json()["status"] == "reported"
    assert admin_detail.json()["report_state"] == "reported"
    assert admin_detail.json()["source_type"] == "plaza_comment"
    assert admin_requests.status_code == 200
    assert any(item["id"] == created.json()["id"] for item in admin_requests.json())


def test_match_expand_context_request_is_free_for_vip_user():
    before = client.get("/me/status").json()["user"]["drift_coins"]
    response = client.post("/chat/match-expand-requests", json={"target_user_id": CREATOR_006_ID})
    after = client.get("/me/status").json()["user"]["drift_coins"]
    thread = client.post(f"/conversations/{response.json()['thread_id']}/read")

    assert response.status_code == 200
    data = response.json()
    assert data["gate"] == "vip"
    assert data["cost_coins"] == 0
    assert data["remaining_drift_coins"] == before
    assert after == before
    assert data["thread_id"]
    assert data["request"]["status"] == "active"
    assert data["request"]["conversation_id"] == data["thread_id"]
    assert data["request"]["source_type"] == "match_expand"
    assert data["request"]["source_id"] == f"nearby:{CREATOR_006_ID}"
    assert thread.status_code == 200
    assert thread.json()["participant_user_id"] == CREATOR_006_ID
    assert thread.json()["participant_avatar_url"].startswith("https://api.dicebear.com/9.x/open-peeps/svg")


def test_match_expand_context_request_costs_five_coins_for_non_vip_user():
    headers = {"X-User-Id": CREATOR_002_ID}
    before = client.get("/me/status", headers=headers).json()["user"]["drift_coins"]
    response = client.post("/chat/match-expand-requests", json={"target_user_id": CREATOR_003_ID}, headers=headers)
    after = client.get("/me/status", headers=headers).json()["user"]["drift_coins"]

    assert response.status_code == 200
    data = response.json()
    assert data["gate"] == "drift_coins"
    assert data["cost_coins"] == 5
    assert data["remaining_drift_coins"] == before - 5
    assert after == before - 5
    assert data["thread_id"]
    assert data["request"]["status"] == "active"
    assert data["request"]["conversation_id"] == data["thread_id"]
    assert data["request"]["source_type"] == "match_expand"
    assert data["request"]["source_id"] == f"nearby:{CREATOR_003_ID}"


def test_match_expand_context_request_reuses_existing_chat_without_second_charge():
    headers = {"X-User-Id": CREATOR_002_ID}
    before = client.get("/me/status", headers=headers).json()["user"]["drift_coins"]
    first = client.post("/chat/match-expand-requests", json={"target_user_id": CREATOR_004_ID}, headers=headers)
    after_first = client.get("/me/status", headers=headers).json()["user"]["drift_coins"]
    second = client.post("/chat/match-expand-requests", json={"target_user_id": CREATOR_004_ID}, headers=headers)
    after_second = client.get("/me/status", headers=headers).json()["user"]["drift_coins"]

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["request"]["id"] == second.json()["request"]["id"]
    assert first.json()["thread_id"] == second.json()["thread_id"]
    assert first.json()["cost_coins"] == 5
    assert second.json()["cost_coins"] == 0
    assert second.json()["request"]["status"] == "active"
    assert before - after_first == 5
    assert after_second == after_first


def test_context_chat_block_prevents_messages():
    target_headers = {"X-User-Id": CREATOR_004_ID}
    created = client.post(
        "/chat/context-requests",
        json={
            "target_user_id": CREATOR_004_ID,
            "source_type": "treehole_comment",
            "source_id": "tree_001:comment_contract_001",
            "initiator_action": "continue_chat",
            "evidence_id": "tree_comment_contract_001",
        },
    )
    accepted = client.post(
        f"/chat/context-requests/{created.json()['id']}/accept",
        json={"confirm_action": "reply", "evidence_id": "tree_author_reply_contract_001"},
        headers=target_headers,
    )
    conversation_id = accepted.json()["conversation_id"]
    blocked = client.post(
        f"/chat/conversations/{conversation_id}/block",
        json={"target_user_id": DEFAULT_USER_ID, "reason": "不再接收"},
        headers=target_headers,
    )
    denied = client.post(
        f"/chat/conversations/{conversation_id}/messages",
        json={"content_type": "text", "content": "blocked message"},
    )

    assert blocked.status_code == 200
    assert blocked.json()["conversation_status"] == "blocked"
    assert denied.status_code == 403
    assert denied.json()["error"]["code"] == "CHAT_BLOCKED"


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
    chat_rows = chats.json()
    chat = next(item for item in chat_rows if item["thread_id"] == thread["id"])
    assert thread["participant_user_id"] in chat["participant_user_ids"]
    assert chat["participants"]
    assert chat["messages"]

    sources = {item["source"] for item in chat_rows}
    assert {"bottle", "treehole", "plaza", "game_room"}.issubset(sources)
    game_chat = next(item for item in chat_rows if item["source"] == "game_room")
    assert game_chat["messages"]
    assert any(message["type"] == "game_room" for message in game_chat["messages"])
    assert game_chat["discipline_status"] in {"watch", "violation"}
    assert game_chat["discipline_summary"]
    assert game_chat["room_mode"] in {"truth", "dare", "mixed"}


def test_conversation_read_endpoint_clears_thread_unread_count():
    conversations = client.get("/conversations")
    assert conversations.status_code == 200
    rows = conversations.json()
    thread = next((item for item in rows if item["unread_count"] > 0), rows[0])

    marked = client.post(f"/conversations/{thread['id']}/read")
    listed = client.get("/conversations")
    updated = next(item for item in listed.json() if item["id"] == thread["id"])

    assert marked.status_code == 200
    assert marked.json()["id"] == thread["id"]
    assert marked.json()["unread_count"] == 0
    assert updated["unread_count"] == 0


def test_message_read_endpoint_clears_only_one_notification():
    messages = client.get("/messages")
    assert messages.status_code == 200
    unread_messages = [item for item in messages.json() if item["unread"]]
    message = unread_messages[0] if unread_messages else messages.json()[0]

    marked = client.post(f"/messages/{message['id']}/read")
    listed = client.get("/messages")
    updated = next(item for item in listed.json() if item["id"] == message["id"])

    assert marked.status_code == 200
    assert marked.json()["id"] == message["id"]
    assert marked.json()["unread"] is False
    assert updated["unread"] is False


def test_admin_reports_support_evidence_search_filters():
    headers = admin_headers()
    reports = client.get("/admin/reports", headers=headers)
    assert reports.status_code == 200
    rows = reports.json()
    assert rows
    assert all(item["evidence_refs"] for item in rows)

    chat = next(item for item in rows if item["target_type"] == "chat")
    filtered = client.get(
        "/admin/reports",
        params={"target_type": "chat", "status": chat["status"], "q": chat["target_id"]},
        headers=headers,
    )
    assert filtered.status_code == 200
    filtered_rows = filtered.json()
    assert filtered_rows
    assert all(item["target_type"] == "chat" for item in filtered_rows)
    assert all(item["status"] == chat["status"] for item in filtered_rows)
    assert any(chat["target_id"] in item["evidence_refs"] or item["target_id"] == chat["target_id"] for item in filtered_rows)


def test_admin_report_resolve_updates_status_and_writes_audit():
    headers = admin_headers()
    reports = client.get("/admin/reports", headers=headers)
    assert reports.status_code == 200
    report = next(item for item in reports.json() if item["status"] != "resolved")

    resolved = client.post(
        f"/admin/reports/{report['id']}/resolve",
        json={"action": "resolve", "reason": "证据已核对，关闭举报"},
        headers=headers,
    )
    listed = client.get("/admin/reports", headers=headers)
    updated = next(item for item in listed.json() if item["id"] == report["id"])
    audit = client.get("/admin/audit", headers=headers)

    assert resolved.status_code == 200
    assert resolved.json()["report_id"] == report["id"]
    assert resolved.json()["before_status"] == report["status"]
    assert resolved.json()["after_status"] == "resolved"
    assert resolved.json()["audit_id"]
    assert updated["status"] == "resolved"
    assert resolved.json()["audit_id"] in updated["audit_refs"]
    assert any(item["id"] == resolved.json()["audit_id"] and item["action"] == "report_resolve" for item in audit.json())


def test_admin_report_resolve_can_limit_reported_chat_user_and_expose_audit_detail():
    headers = admin_headers()
    reports = client.get("/admin/reports", headers=headers)
    assert reports.status_code == 200
    report = next(item for item in reports.json() if item["target_type"] == "chat")
    chats = client.get("/admin/chats", headers=headers)
    assert chats.status_code == 200
    chat = next(item for item in chats.json() if item["thread_id"] == report["target_id"])
    target_user_id = next(user_id for user_id in chat["participant_user_ids"] if user_id != report["reporter_id"])

    resolved = client.post(
        f"/admin/reports/{report['id']}/resolve",
        json={"action": "resolve", "reason": "聊天违规，限制账号", "penalty_action": "limit_user"},
        headers=headers,
    )
    users = client.get("/admin/users", headers=headers)
    target_user = next(item for item in users.json() if item["id"] == target_user_id)
    audit = client.get("/admin/audit", headers=headers)
    resolve_audit = next(item for item in audit.json() if item["id"] == resolved.json()["audit_id"])

    assert resolved.status_code == 200
    assert resolved.json()["after_status"] == "resolved"
    assert resolved.json()["penalty_action"] == "limit_user"
    assert resolved.json()["penalty_target_user_id"] == target_user_id
    assert resolved.json()["penalty_audit_id"]
    assert target_user["status"] == "limited"
    assert "penalty_action=limit_user" in resolve_audit["detail"]
    assert target_user_id in resolve_audit["detail"]


def test_admin_report_resolve_can_freeze_chat_and_block_new_message():
    headers = admin_headers()
    threads = client.get("/conversations")
    assert threads.status_code == 200
    thread = next(item for item in threads.json() if item["status"] == "active")
    report_created = client.post(
        "/reports",
        json={"target_type": "chat", "target_id": thread["id"], "reason": "LOOP-39 冻结通知测试"},
    )
    assert report_created.status_code == 200
    report = report_created.json()

    resolved = client.post(
        f"/admin/reports/{report['id']}/resolve",
        json={"action": "resolve", "reason": "聊天风险冻结", "penalty_action": "freeze_chat"},
        headers=headers,
    )
    listed = client.get("/admin/reports", params={"q": report["id"]}, headers=headers)
    updated = next(item for item in listed.json() if item["id"] == report["id"])
    denied = client.post(
        f"/conversations/{report['target_id']}/turns",
        json={"body": "frozen chat message"},
    )
    messages = client.get("/messages")
    freeze_notice = next(
        item
        for item in messages.json()
        if item["business_type"] == "chat_freeze" and item["business_id"] == report["target_id"]
    )
    frozen_thread = client.post(f"/conversations/{report['target_id']}/read")
    audit = client.get("/admin/audit", headers=headers)
    resolve_audit = next(item for item in audit.json() if item["id"] == resolved.json()["audit_id"])

    assert resolved.status_code == 200
    assert resolved.json()["after_status"] == "resolved"
    assert resolved.json()["penalty_action"] == "freeze_chat"
    assert resolved.json()["penalty_target_thread_id"] == report["target_id"]
    assert resolved.json()["penalty_audit_id"]
    assert "thread_status:risk_frozen" in updated["evidence_refs"]
    assert denied.status_code == 403
    assert denied.json()["error"]["code"] == "CHAT_RISK_FROZEN"
    assert messages.status_code == 200
    assert "申诉" in freeze_notice["body"]
    assert frozen_thread.status_code == 200
    assert frozen_thread.json()["status"] == "risk_frozen"
    assert "申诉" in frozen_thread.json()["frozen_notice"]
    assert "penalty_action=freeze_chat" in resolve_audit["detail"]
    assert report["target_id"] in resolve_audit["detail"]


def test_admin_report_resolve_can_offline_reported_content_and_expose_audit_detail():
    headers = admin_headers()
    bottle = client.post("/bottles", json={"content": "LOOP-43 被举报下线的漂流瓶"})
    plaza = client.post("/plaza/posts", json={"content": "LOOP-43 被举报下线的广场帖子", "media_type": "text", "media_count": 0})
    comment = client.post(f"/plaza/posts/{plaza.json()['id']}/comments", json={"content": "LOOP-43 被举报下线的留言"})
    comment_id = next(item["id"] for item in client.get(f"/plaza/posts/{plaza.json()['id']}/comments").json() if item["content"] == "LOOP-43 被举报下线的留言")

    targets = [
        ("bottle", bottle.json()["id"], "bottle"),
        ("plaza", plaza.json()["id"], "plaza"),
        ("reply", comment_id, "plaza_comment"),
    ]
    resolved_payloads = []
    for target_type, target_id, content_type in targets:
        report = client.post(
            "/reports",
            json={"target_type": target_type, "target_id": target_id, "reason": f"LOOP-43 offline {content_type}"},
        )
        assert report.status_code == 200
        resolved = client.post(
            f"/admin/reports/{report.json()['id']}/resolve",
            json={"action": "resolve", "reason": "举报属实，下线目标内容", "penalty_action": "offline_content"},
            headers=headers,
        )
        assert resolved.status_code == 200
        assert resolved.json()["penalty_action"] == "offline_content"
        assert resolved.json()["penalty_target_content_id"] == target_id
        assert resolved.json()["penalty_target_content_type"] == content_type
        assert resolved.json()["penalty_audit_id"]
        resolved_payloads.append((report.json()["id"], target_id, content_type, resolved.json()))

    bottles = client.get("/bottles")
    plaza_posts = client.get("/plaza/posts")
    comments = client.get(f"/plaza/posts/{plaza.json()['id']}/comments")
    reports = client.get("/admin/reports", params={"q": "LOOP-43 offline"}, headers=headers)
    messages = client.get("/messages")
    audit = client.get("/admin/audit", headers=headers)

    assert bottles.status_code == 200
    assert plaza_posts.status_code == 200
    assert comments.status_code == 200
    assert all(item["id"] != bottle.json()["id"] for item in bottles.json())
    assert all(item["id"] != plaza.json()["id"] for item in plaza_posts.json())
    assert all(item["id"] != comment_id for item in comments.json())
    assert len(reports.json()) >= 3
    assert all("content_status:rejected" in item["evidence_refs"] for item in reports.json() if item["reason"].startswith("LOOP-43 offline"))
    assert any(item["business_type"] == "content_offline" and item["business_id"] == bottle.json()["id"] for item in messages.json())
    assert any(item["action"] == "report_penalty_offline_content" for item in audit.json())
    for _, target_id, content_type, resolved in resolved_payloads:
        penalty_audit = next(item for item in audit.json() if item["id"] == resolved["penalty_audit_id"])
        resolve_audit = next(item for item in audit.json() if item["id"] == resolved["audit_id"])
        assert penalty_audit["target_type"] == content_type
        assert penalty_audit["target_id"] == target_id
        assert "after_status=rejected" in penalty_audit["detail"]
        assert f"penalty_target_content_id={target_id}" in resolve_audit["detail"]


def test_admin_report_restore_chat_reactivates_thread_and_writes_audit():
    headers = admin_headers()
    thread = next(item for item in client.get("/conversations").json() if item["status"] == "active")
    report = client.post(
        "/reports",
        json={"target_type": "chat", "target_id": thread["id"], "reason": "LOOP-40 恢复聊天测试"},
    ).json()
    frozen = client.post(
        f"/admin/reports/{report['id']}/resolve",
        json={"action": "resolve", "reason": "先冻结再恢复", "penalty_action": "freeze_chat"},
        headers=headers,
    )
    restored = client.post(
        f"/admin/reports/{report['id']}/restore",
        json={"reason": "误冻结，恢复聊天"},
        headers=headers,
    )
    restored_thread = client.post(f"/conversations/{thread['id']}/read")
    sent = client.post(
        f"/conversations/{thread['id']}/turns",
        json={"body": "restored chat message"},
    )
    messages = client.get("/messages")
    restore_notice = next(
        item
        for item in messages.json()
        if item["business_type"] == "chat_restore" and item["business_id"] == thread["id"]
    )
    audit = client.get("/admin/audit", headers=headers)
    restore_audit = next(item for item in audit.json() if item["id"] == restored.json()["audit_id"])

    assert frozen.status_code == 200
    assert restored.status_code == 200
    assert restored.json()["thread_id"] == thread["id"]
    assert restored.json()["before_thread_status"] == "risk_frozen"
    assert restored.json()["after_thread_status"] == "active"
    assert restored_thread.json()["status"] == "active"
    assert sent.status_code == 200
    assert sent.json()["last_message"] == "restored chat message"
    assert "恢复" in restore_notice["title"]
    assert restore_audit["action"] == "report_restore_chat"
    assert "after_status=active" in restore_audit["detail"]


def test_chat_appeal_submit_approve_and_reject_contract():
    headers = admin_headers()

    approve_user_headers = {"X-Client-Id": "loop42_appeal_approve_user"}
    approve_thread = client.post(
        "/chat/match-expand-requests",
        json={"target_user_id": CREATOR_006_ID},
        headers=approve_user_headers,
    ).json()["thread_id"]
    approve_report = client.post(
        "/reports",
        json={"target_type": "chat", "target_id": approve_thread, "reason": "LOOP-42 申诉通过测试"},
        headers=approve_user_headers,
    ).json()
    client.post(
        f"/admin/reports/{approve_report['id']}/resolve",
        json={"action": "resolve", "reason": "先冻结用于申诉通过", "penalty_action": "freeze_chat"},
        headers=headers,
    )
    submitted = client.post(
        f"/conversations/{approve_thread}/appeal",
        json={"reason": "这是误冻结，请恢复聊天"},
        headers=approve_user_headers,
    )
    listed = client.get("/admin/chat-appeals", headers=headers)
    approved = client.post(
        f"/admin/chat-appeals/{submitted.json()['id']}/review",
        json={"action": "approve", "reason": "复核通过，恢复聊天"},
        headers=headers,
    )
    approved_thread = client.post(f"/conversations/{approve_thread}/read", headers=approve_user_headers)
    approved_messages = client.get("/messages", headers=approve_user_headers)

    reject_user_headers = {"X-Client-Id": "loop42_appeal_reject_user"}
    reject_thread = client.post(
        "/chat/match-expand-requests",
        json={"target_user_id": CREATOR_004_ID},
        headers=reject_user_headers,
    ).json()["thread_id"]
    reject_report = client.post(
        "/reports",
        json={"target_type": "chat", "target_id": reject_thread, "reason": "LOOP-42 申诉驳回测试"},
        headers=reject_user_headers,
    ).json()
    client.post(
        f"/admin/reports/{reject_report['id']}/resolve",
        json={"action": "resolve", "reason": "先冻结用于申诉驳回", "penalty_action": "freeze_chat"},
        headers=headers,
    )
    rejected_submit = client.post(
        f"/conversations/{reject_thread}/appeal",
        json={"reason": "我不同意冻结"},
        headers=reject_user_headers,
    )
    rejected = client.post(
        f"/admin/chat-appeals/{rejected_submit.json()['id']}/review",
        json={"action": "reject", "reason": "证据成立，维持冻结"},
        headers=headers,
    )
    rejected_thread = client.post(f"/conversations/{reject_thread}/read", headers=reject_user_headers)
    rejected_messages = client.get("/messages", headers=reject_user_headers)
    audit = client.get("/admin/audit", headers=headers)

    assert submitted.status_code == 200
    assert submitted.json()["status"] == "pending"
    assert submitted.json()["thread_id"] == approve_thread
    assert submitted.json()["audit_refs"]
    assert any(item["id"] == submitted.json()["id"] for item in listed.json())
    assert approved.status_code == 200
    assert approved.json()["after_status"] == "approved"
    assert approved.json()["thread_status"] == "active"
    assert approved_thread.json()["status"] == "active"
    assert any(item["business_type"] == "chat_appeal_approved" and item["business_id"] == approve_thread for item in approved_messages.json())
    assert rejected.status_code == 200
    assert rejected.json()["after_status"] == "rejected"
    assert rejected.json()["thread_status"] == "risk_frozen"
    assert rejected_thread.json()["status"] == "risk_frozen"
    assert any(item["business_type"] == "chat_appeal_rejected" and item["business_id"] == reject_thread for item in rejected_messages.json())
    assert any(item["id"] == approved.json()["audit_id"] and item["action"] == "chat_appeal_approve" for item in audit.json())
    assert any(item["id"] == rejected.json()["audit_id"] and item["action"] == "chat_appeal_reject" for item in audit.json())


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
    audit = client.get("/admin/audit", headers=headers)
    wallet = client.get("/admin/wallet", headers=headers)
    verification = client.get("/admin/verification", headers=headers)
    referral = client.get("/admin/referral", headers=headers)
    nearby = client.get("/admin/nearby", headers=headers)
    plaza = client.get("/admin/plaza", headers=headers)
    content = client.get("/admin/content", headers=headers)
    users = client.get("/admin/users", headers=headers)

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


def test_friend_request_notification_keeps_context_chat_rule():
    target_user_id = "200000000006"
    response = client.post("/relations/friend-request", json={"target_user_id": target_user_id})
    messages = client.get("/messages")

    assert response.status_code == 200
    assert messages.status_code == 200
    assert any(
        item["title"] == "好友申请已发送"
        and "明确互动上下文内仍可按规则继续聊" in item["body"]
        and "通过后才会打开私信" not in item["body"]
        for item in messages.json()
    )


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
    reward_config = client.get("/admin/reward-config", headers=headers).json()
    update = client.patch("/admin/reward-config", json=reward_config, headers=headers)
    logout = client.post("/admin/auth/logout", headers=headers)
    audit = client.get("/admin/audit", headers=headers)

    assert me.status_code == 200
    assert me.json()["roles"] == ["admin", "moderator"]
    assert logout.status_code == 200
    assert logout.json()["status"] == "logged_out"
    assert update.status_code == 200
    assert any(item["action"] == "update_reward_config" for item in audit.json())


def test_admin_ad_config_controls_reward_video_bridge():
    headers = admin_headers()
    config = client.get("/admin/reward-config", headers=headers).json()
    config.update(
        {
            "ad_cooldown_minutes": 0,
            "ad_reward_per_quota": 2,
            "ad_display_type": "video",
            "ad_provider": "loop29_alliance",
            "ad_placement_id": "loop29_reward_video",
            "ad_title": "LOOP-29 激励视频",
            "ad_description": "倒计时完成后发放次数",
            "ad_media_url": "https://example.com/reward.mp4",
            "ad_click_url": "https://example.com/reward",
            "ad_countdown_seconds": 3,
            "mini_program_app_id": "wx-loop29",
            "mini_program_path": "pages/ad/reward",
        }
    )
    update = client.patch("/admin/reward-config", json=config, headers=headers)
    user_headers = {"X-Client-Id": "loop29_ad_user"}
    before = client.get("/me/status", headers=user_headers).json()
    prepared = client.post("/ads/reward/prepare", headers=user_headers)
    committed = client.post(
        "/ads/reward/commit",
        json={"reward_session_id": prepared.json()["reward_session_id"], "completed": True},
        headers=user_headers,
    )
    audit = client.get("/admin/audit", headers=headers)

    assert update.status_code == 200
    assert update.json()["ad_provider"] == "loop29_alliance"
    assert before["ad_reward"]["provider"] == "loop29_alliance"
    assert before["ad_reward"]["placement_id"] == "loop29_reward_video"
    assert before["ad_reward"]["countdown_seconds"] == 3
    assert before["ad_reward"]["mini_program_path"] == "pages/ad/reward"
    assert prepared.status_code == 200
    assert prepared.json()["reward_per_quota"] == 2
    assert prepared.json()["provider"] == "loop29_alliance"
    assert committed.status_code == 200
    assert committed.json()["quotas"]["fish_bottle"]["remaining"] == before["quotas"]["fish_bottle"]["remaining"] + 2
    assert any(item["action"] == "update_ad_reward_config" for item in audit.json())


def test_admin_write_requires_token_with_unified_error():
    response = client.post("/admin/moderation/job_auth_required", json={"action": "reject"})

    assert response.status_code == 401
    assert response.json() == {
        "error": {
            "code": "ADMIN_UNAUTHORIZED",
            "message": "Admin bearer token is required",
        }
    }


def test_admin_reads_require_token_and_roles_are_enforced():
    no_auth = client.get("/admin/summary")
    bad_token = client.get("/admin/summary", headers={"Authorization": "Bearer invalid-admin-token"})
    moderator_login = client.post(
        "/admin/auth/login",
        json={"username": "moderator", "password": "moderator_mock_password"},
    )
    moderator_headers = {"Authorization": f"Bearer {moderator_login.json()['access_token']}"}
    moderator_summary = client.get("/admin/summary", headers=moderator_headers)
    reward_config = client.get("/admin/reward-config", headers=moderator_headers)
    forbidden_update = client.patch("/admin/reward-config", json=reward_config.json(), headers=moderator_headers)

    assert no_auth.status_code == 401
    assert no_auth.json()["error"]["code"] == "ADMIN_UNAUTHORIZED"
    assert bad_token.status_code == 401
    assert bad_token.json()["error"]["code"] == "ADMIN_UNAUTHORIZED"
    assert moderator_login.status_code == 200
    assert moderator_login.json()["admin"]["roles"] == ["moderator"]
    assert moderator_summary.status_code == 200
    assert forbidden_update.status_code == 403
    assert forbidden_update.json()["error"]["code"] == "ADMIN_FORBIDDEN"


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
