from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app import plaza_store
from app.mock_store import iso_now, user
from app.routes.wallet import nearby_users
from app.schemas import NearbyUser, PlazaCommentOut, PlazaCommentRequest, PlazaCreateRequest, PlazaMediaOut, PlazaPost

router = APIRouter(tags=["plaza"])

CITY_ALL = "\u5168\u56fd"
AGE_ALL = "\u5168\u90e8"
GENDER_FEMALE = "\u5973"
GENDER_MALE = "\u7537"


def normalize_gender(value: str | None) -> str | None:
    if value in (GENDER_FEMALE, "female", "F"):
        return "female"
    if value in (GENDER_MALE, "male", "M"):
        return "male"
    return None


def parse_age_range(value: str | None) -> tuple[int, int] | None:
    if not value or value in (AGE_ALL, "all"):
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


def can_view_comment(comment: PlazaCommentOut, post: PlazaPost, viewer_id: str) -> bool:
    if not comment.hidden_for_owner_only:
        return True
    return viewer_id == post.author_id


def visible_comment_for_viewer(comment: PlazaCommentOut, post: PlazaPost, viewer_id: str) -> PlazaCommentOut | None:
    if not can_view_comment(comment, post, viewer_id):
        return None
    if not comment.hidden_for_owner_only:
        return comment
    return comment.model_copy(
        update={
            "author_id": "anonymous",
            "author_name": "\u533f\u540d\u7559\u8a00",
            "icon_text": "\u533f",
            "author_gender": "unknown",
            "author_age_range": None,
            "author_verified": False,
            "author_city": None,
        }
    )


@router.get("/plaza/posts", response_model=list[PlazaPost])
def list_plaza_posts(city: str | None = None, gender: str | None = None, age_range: str | None = None) -> list[PlazaPost]:
    result = plaza_store.list_posts()
    normalized_gender = normalize_gender(gender)
    if city and city not in (CITY_ALL, "all"):
        result = [item for item in result if item.city == city]
    if normalized_gender:
        result = [item for item in result if item.gender == normalized_gender]
    if parse_age_range(age_range):
        result = [item for item in result if age_ranges_overlap(item.age_range, age_range)]
    return plaza_store.increment_views([item.id for item in result], user.id, f"plaza_view_{uuid4().hex}")


@router.get("/plaza/posts/{post_id}", response_model=PlazaPost)
def get_plaza_post(post_id: str) -> PlazaPost:
    post = plaza_store.get_post(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="PLAZA_POST_NOT_FOUND")
    return post


@router.post("/plaza/posts", response_model=PlazaPost)
def create_plaza_post(payload: PlazaCreateRequest) -> PlazaPost:
    content = payload.content.strip()
    if not content:
        raise HTTPException(status_code=422, detail="EMPTY_PLAZA_CONTENT")

    post_id = f"plaza_{uuid4().hex}"
    media_items = []
    for index, media in enumerate(payload.media, start=1):
        media_items.append(
            PlazaMediaOut(
                **media.model_dump(exclude={"storage_key"}),
                id=f"plaza_media_{uuid4().hex}",
                post_id=post_id,
                owner_id=user.id,
                storage_key=media.storage_key or f"plaza/{post_id}_{index}",
                created_at=iso_now(),
            )
        )
    if not media_items and payload.media_type != "text" and payload.media_count > 0:
        default_media = default_media_for_type(payload.media_type, post_id)
        media_items.append(
            PlazaMediaOut(
                id=f"plaza_media_{uuid4().hex}",
                post_id=post_id,
                owner_id=user.id,
                media_type=payload.media_type,
                url=default_media["url"],
                storage_key=f"plaza/{post_id}_01",
                mime_type=default_media["mime_type"],
                size_bytes=0,
                duration_seconds=default_media["duration_seconds"],
                width=default_media["width"],
                height=default_media["height"],
                created_at=iso_now(),
            )
        )

    post = PlazaPost(
        id=post_id,
        author_id=user.id,
        author_name=user.nickname,
        icon_text=user.avatar_text,
        topic="\u4eca\u65e5\u52a8\u6001",
        content=content,
        media_type=payload.media_type,
        media_count=len(payload.media) if payload.media else payload.media_count,
        gender=user.gender,
        verified=bool(user.face_verified and user.gender_verified),
        city=user.city or "\u676d\u5dde",
        age_range="25-30",
        view_count=0,
        like_count=0,
        comment_count=0,
        media=media_items,
        distance_text="\u521a\u521a",
        created_at=iso_now(),
    )
    return plaza_store.create_post(post, media_items)


@router.post("/plaza/posts/{post_id}/comments", response_model=PlazaPost)
def comment_plaza_post(post_id: str, payload: PlazaCommentRequest) -> PlazaPost:
    content = payload.content.strip()
    if not content:
        raise HTTPException(status_code=422, detail="EMPTY_PLAZA_COMMENT")
    post = plaza_store.get_post(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="PLAZA_POST_NOT_FOUND")
    updated_post = plaza_store.add_comment(
        PlazaCommentOut(
            id=f"plaza_comment_{uuid4().hex}",
            post_id=post_id,
            author_id=user.id,
            author_name=user.nickname,
            icon_text=user.avatar_text,
            author_gender=user.gender,
            author_age_range="25-30",
            author_verified=bool(user.face_verified and user.gender_verified),
            author_city=user.city,
            content=content,
            hidden_for_owner_only=payload.hidden_for_owner_only,
            visible_to_owner_only=payload.hidden_for_owner_only,
            created_at=iso_now(),
        ),
    )
    if updated_post is None:
        raise HTTPException(status_code=404, detail="PLAZA_POST_NOT_FOUND")
    return updated_post


@router.get("/plaza/posts/{post_id}/comments", response_model=list[PlazaCommentOut])
def list_plaza_comments(post_id: str, viewer_id: str | None = None) -> list[PlazaCommentOut]:
    post = plaza_store.get_post(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="PLAZA_POST_NOT_FOUND")
    current_viewer_id = viewer_id or user.id
    visible_comments = []
    for item in plaza_store.list_comments(post_id):
        visible_comment = visible_comment_for_viewer(item, post, current_viewer_id)
        if visible_comment:
            visible_comments.append(visible_comment)
    return visible_comments


@router.post("/plaza/posts/{post_id}/like", response_model=PlazaPost)
def like_plaza_post(post_id: str) -> PlazaPost:
    post = plaza_store.toggle_like_post(post_id, user.id, f"plaza_like_{uuid4().hex}")
    if post is None:
        raise HTTPException(status_code=404, detail="PLAZA_POST_NOT_FOUND")
    return post


def default_media_for_type(media_type: str, post_id: str) -> dict[str, int | str | None]:
    if media_type == "voice":
        return {
            "url": "https://interactive-examples.mdn.mozilla.net/media/cc0-audio/t-rex-roar.mp3",
            "mime_type": "audio/mpeg",
            "duration_seconds": 2,
            "width": None,
            "height": None,
        }
    if media_type == "video":
        return {
            "url": "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
            "mime_type": "video/mp4",
            "duration_seconds": 5,
            "width": 1080,
            "height": 1920,
        }
    return {
        "url": f"https://picsum.photos/seed/{post_id}/900/1200",
        "mime_type": "image/jpeg",
        "duration_seconds": None,
        "width": 900,
        "height": 1200,
    }


@router.get("/nearby/users", response_model=list[NearbyUser])
def list_nearby_users(gender: str | None = None, age_range: str | None = None, distance_km: float | None = None) -> list[NearbyUser]:
    result = nearby_users
    normalized_gender = normalize_gender(gender)
    if normalized_gender:
        result = [item for item in result if item.gender == normalized_gender]
    if age_range and age_range not in (AGE_ALL, "all"):
        result = [item for item in result if item.age_range == age_range]
    if distance_km is not None:
        result = [item for item in result if (item.distance_km or 999) <= distance_km]
    return result
