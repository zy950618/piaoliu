import os
import sqlite3

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def admin_headers() -> dict[str, str]:
    response = client.post("/admin/auth/login", json={"username": "admin", "password": "admin_mock_password"})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_me_status_contains_quota_and_reward_state():
    response = client.get("/me/status")
    assert response.status_code == 200
    data = response.json()
    assert "fish_bottle" in data["quotas"]
    assert data["ad_reward"]["reward_per_quota"] == 1
    assert data["checkin"]["week_rewards"] == [10, 10, 30, 10, 10, 30, 100]


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
    assert "view_count" in plaza.json()[0]
    assert "media_type" in plaza.json()[0]
    assert "media" in plaza.json()[0]
    assert plaza.json()[0]["media"][0]["owner_id"] == plaza.json()[0]["author_id"]
    assert plaza.json()[0]["media"][0]["url"].startswith("https://")
    assert {item["media_type"] for post in plaza.json() for item in post["media"]} >= {"image", "voice", "video"}


def test_plaza_publish_contract():
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
        view_count = conn.execute("select count(*) from plaza_view_events where post_id = ?", (post_id,)).fetchone()[0]

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
            (post_id, "user_mock_001"),
        ).fetchone()[0]
    assert like_rows == 0


def test_plaza_hidden_comments_visibility_contract():
    post_id = "plaza_001"
    post_detail = client.get(f"/plaza/posts/{post_id}")
    default_comments = client.get(f"/plaza/posts/{post_id}/comments")
    owner_comments = client.get(f"/plaza/posts/{post_id}/comments", params={"viewer_id": "creator_001"})
    hidden = client.post(
        f"/plaza/posts/{post_id}/comments",
        json={"content": "这条留言只给发布者看。", "hidden_for_owner_only": True},
    )
    commenter_comments = client.get(f"/plaza/posts/{post_id}/comments", params={"viewer_id": "user_mock_001"})
    owner_comments_after = client.get(f"/plaza/posts/{post_id}/comments", params={"viewer_id": "creator_001"})

    assert post_detail.status_code == 200
    assert post_detail.json()["id"] == post_id
    assert post_detail.json()["author_id"] == "creator_001"
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
    target_user_id = "creator_004"
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


def test_backend_infrastructure_placeholders_import_without_connections():
    from app import db
    from app.models import AdminAuditLog, Base, Bottle, BottleReply, Follow, PlazaComment, PlazaLike, PlazaMedia, PlazaPost, User
    from app.redis import get_redis_client
    from app.settings import get_settings

    settings = get_settings()
    redis_client = get_redis_client()

    assert settings.database_url.startswith("postgresql+asyncpg://")
    assert db.engine.url.drivername == "postgresql+asyncpg"
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
