import os
import sqlite3
from pathlib import Path
from threading import Lock

from app.mock_store import iso_now, user
from app.schemas import PlazaCommentOut, PlazaMediaOut, PlazaPost

DB_PATH = Path(
    os.getenv(
        "PLAZA_SQLITE_PATH",
        str(Path(__file__).resolve().parents[1] / "runtime" / "plaza.sqlite3"),
    )
)
_LOCK = Lock()


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_plaza_store() -> None:
    with _LOCK, _connect() as conn:
        conn.executescript(
            """
            create table if not exists plaza_posts (
              id text primary key,
              display_order integer not null default 0,
              author_id text not null,
              author_name text not null,
              icon_text text not null,
              topic text not null,
              content text not null,
              media_type text not null default 'text',
              media_count integer not null default 0,
              gender text not null default 'unknown',
              verified integer not null default 0,
              city text,
              age_range text,
              view_count integer not null default 0,
              like_count integer not null default 0,
              comment_count integer not null default 0,
              comment_preview text,
              distance_text text,
              created_at text not null
            );
            create table if not exists plaza_media (
              id text primary key,
              post_id text not null,
              owner_id text not null,
              media_type text not null,
              url text not null,
              storage_key text,
              mime_type text not null,
              size_bytes integer,
              duration_seconds integer,
              width integer,
              height integer,
              created_at text not null
            );
            create table if not exists plaza_comments (
              id text primary key,
              post_id text not null,
              author_id text not null,
              author_name text not null,
              icon_text text not null,
              author_gender text not null default 'unknown',
              author_age_range text,
              author_verified integer not null default 0,
              author_city text,
              content text not null,
              hidden_for_owner_only integer not null default 0,
              visible_to_owner_only integer not null default 0,
              created_at text not null
            );
            create table if not exists plaza_likes (
              id text primary key,
              post_id text not null,
              user_id text not null,
              created_at text not null
            );
            create table if not exists plaza_view_events (
              id text primary key,
              post_id text not null,
              user_id text not null,
              created_at text not null
            );
            """
        )
        _ensure_comment_profile_columns(conn)
        if conn.execute("select count(*) from plaza_posts").fetchone()[0] == 0:
            _seed(conn)
        else:
            _sync_seed_comments(conn)
            _backfill_comment_profiles(conn)


def _ensure_comment_profile_columns(conn: sqlite3.Connection) -> None:
    columns = {row["name"] for row in conn.execute("pragma table_info(plaza_comments)").fetchall()}
    migrations = [
        ("author_gender", "alter table plaza_comments add column author_gender text not null default 'unknown'"),
        ("author_age_range", "alter table plaza_comments add column author_age_range text"),
        ("author_verified", "alter table plaza_comments add column author_verified integer not null default 0"),
        ("author_city", "alter table plaza_comments add column author_city text"),
    ]
    for column, statement in migrations:
        if column not in columns:
            conn.execute(statement)


def _seed(conn: sqlite3.Connection) -> None:
    from app.routes.wallet import plaza_comments, plaza_media, plaza_posts

    for index, post in enumerate(plaza_posts):
        _insert_post(conn, post, display_order=(len(plaza_posts) - index) * 100)
    for media in plaza_media:
        _insert_media(conn, media)
    for comment in plaza_comments:
        _insert_comment(conn, comment)
    _refresh_comment_summaries(conn)


def _sync_seed_comments(conn: sqlite3.Connection) -> None:
    from app.routes.wallet import plaza_comments

    changed = False
    for comment in plaza_comments:
        if conn.execute("select 1 from plaza_comments where id = ?", (comment.id,)).fetchone():
            continue
        if conn.execute("select 1 from plaza_posts where id = ?", (comment.post_id,)).fetchone() is None:
            continue
        _insert_comment(conn, comment)
        changed = True
    if changed:
        _refresh_comment_summaries(conn)


def _refresh_comment_summaries(conn: sqlite3.Connection) -> None:
    post_ids = [row["id"] for row in conn.execute("select id from plaza_posts").fetchall()]
    for post_id in post_ids:
        comment_count = conn.execute(
            "select count(*) from plaza_comments where post_id = ?",
            (post_id,),
        ).fetchone()[0]
        preview_row = conn.execute(
            """
            select content from plaza_comments
            where post_id = ? and hidden_for_owner_only = 0
            order by created_at desc, rowid desc
            limit 1
            """,
            (post_id,),
        ).fetchone()
        conn.execute(
            "update plaza_posts set comment_count = ?, comment_preview = ? where id = ?",
            (comment_count, preview_row["content"] if preview_row else None, post_id),
        )


def _comment_author_profile(conn: sqlite3.Connection, author_id: str) -> dict[str, str | bool | None]:
    if author_id == user.id:
        return {
            "gender": user.gender,
            "age_range": "25-30",
            "verified": bool(user.face_verified and user.gender_verified),
            "city": user.city,
        }
    post_row = conn.execute(
        "select gender, age_range, verified, city from plaza_posts where author_id = ? order by display_order desc limit 1",
        (author_id,),
    ).fetchone()
    if post_row:
        return {
            "gender": post_row["gender"],
            "age_range": post_row["age_range"],
            "verified": bool(post_row["verified"]),
            "city": post_row["city"],
        }
    fallback_profiles = {
        "creator_002": ("female", "18-24", True, "杭州"),
        "creator_005": ("female", "22-26", True, "成都"),
        "creator_007": ("female", "27-32", True, "北京"),
        "creator_008": ("unknown", "未知", False, "厦门"),
        "creator_009": ("male", "25-30", False, "深圳"),
    }
    gender, age_range, verified, city = fallback_profiles.get(author_id, ("unknown", None, False, None))
    return {"gender": gender, "age_range": age_range, "verified": verified, "city": city}


def _backfill_comment_profiles(conn: sqlite3.Connection) -> None:
    rows = conn.execute(
        """
        select id, author_id from plaza_comments
        where author_gender = 'unknown' or author_age_range is null or author_city is null
        """
    ).fetchall()
    for row in rows:
        profile = _comment_author_profile(conn, row["author_id"])
        conn.execute(
            """
            update plaza_comments
            set author_gender = ?, author_age_range = ?, author_verified = ?, author_city = ?
            where id = ?
            """,
            (
                profile["gender"] or "unknown",
                profile["age_range"],
                int(bool(profile["verified"])),
                profile["city"],
                row["id"],
            ),
        )


def _insert_post(conn: sqlite3.Connection, post: PlazaPost, display_order: int) -> None:
    conn.execute(
        """
        insert into plaza_posts (
          id, display_order, author_id, author_name, icon_text, topic, content,
          media_type, media_count, gender, verified, city, age_range, view_count,
          like_count, comment_count, comment_preview, distance_text, created_at
        ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            post.id,
            display_order,
            post.author_id,
            post.author_name,
            post.icon_text,
            post.topic,
            post.content,
            post.media_type,
            post.media_count,
            post.gender,
            int(post.verified),
            post.city,
            post.age_range,
            post.view_count,
            post.like_count,
            post.comment_count,
            post.comment_preview,
            post.distance_text,
            post.created_at,
        ),
    )


def _insert_media(conn: sqlite3.Connection, media: PlazaMediaOut) -> None:
    conn.execute(
        """
        insert into plaza_media (
          id, post_id, owner_id, media_type, url, storage_key, mime_type,
          size_bytes, duration_seconds, width, height, created_at
        ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            media.id,
            media.post_id,
            media.owner_id,
            media.media_type,
            media.url,
            media.storage_key,
            media.mime_type,
            media.size_bytes,
            media.duration_seconds,
            media.width,
            media.height,
            media.created_at,
        ),
    )


def _insert_comment(conn: sqlite3.Connection, comment: PlazaCommentOut) -> None:
    conn.execute(
        """
        insert into plaza_comments (
          id, post_id, author_id, author_name, icon_text,
          author_gender, author_age_range, author_verified, author_city, content,
          hidden_for_owner_only, visible_to_owner_only, created_at
        ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            comment.id,
            comment.post_id,
            comment.author_id,
            comment.author_name,
            comment.icon_text,
            comment.author_gender,
            comment.author_age_range,
            int(comment.author_verified),
            comment.author_city,
            comment.content,
            int(comment.hidden_for_owner_only),
            int(comment.visible_to_owner_only),
            comment.created_at,
        ),
    )


def list_posts() -> list[PlazaPost]:
    init_plaza_store()
    with _LOCK, _connect() as conn:
        rows = conn.execute("select * from plaza_posts order by display_order desc, created_at desc").fetchall()
        return [_row_to_post(conn, row) for row in rows]


def get_post(post_id: str) -> PlazaPost | None:
    init_plaza_store()
    with _LOCK, _connect() as conn:
        row = conn.execute("select * from plaza_posts where id = ?", (post_id,)).fetchone()
        return _row_to_post(conn, row) if row else None


def create_post(post: PlazaPost, media_items: list[PlazaMediaOut]) -> PlazaPost:
    init_plaza_store()
    with _LOCK, _connect() as conn:
        max_order = conn.execute("select coalesce(max(display_order), 0) from plaza_posts").fetchone()[0]
        _insert_post(conn, post, display_order=max_order + 100)
        for media in media_items:
            _insert_media(conn, media)
        conn.commit()
        return _row_to_post(conn, conn.execute("select * from plaza_posts where id = ?", (post.id,)).fetchone())


def add_comment(comment: PlazaCommentOut) -> PlazaPost | None:
    init_plaza_store()
    with _LOCK, _connect() as conn:
        post = conn.execute("select * from plaza_posts where id = ?", (comment.post_id,)).fetchone()
        if post is None:
            return None
        _insert_comment(conn, comment)
        preview = None if comment.hidden_for_owner_only else comment.content
        if preview:
            conn.execute(
                "update plaza_posts set comment_count = comment_count + 1, comment_preview = ? where id = ?",
                (preview, comment.post_id),
            )
        else:
            conn.execute("update plaza_posts set comment_count = comment_count + 1 where id = ?", (comment.post_id,))
        conn.commit()
        return _row_to_post(conn, conn.execute("select * from plaza_posts where id = ?", (comment.post_id,)).fetchone())


def list_comments(post_id: str) -> list[PlazaCommentOut]:
    init_plaza_store()
    with _LOCK, _connect() as conn:
        rows = conn.execute(
            "select * from plaza_comments where post_id = ? order by created_at desc, rowid desc",
            (post_id,),
        ).fetchall()
        return [_row_to_comment(row) for row in rows]


def toggle_like_post(post_id: str, user_id: str, like_id: str) -> PlazaPost | None:
    init_plaza_store()
    with _LOCK, _connect() as conn:
        if conn.execute("select 1 from plaza_posts where id = ?", (post_id,)).fetchone() is None:
            return None
        existing_like_count = conn.execute(
            "select count(*) from plaza_likes where post_id = ? and user_id = ?",
            (post_id, user_id),
        ).fetchone()[0]
        if existing_like_count:
            conn.execute("delete from plaza_likes where post_id = ? and user_id = ?", (post_id, user_id))
            conn.execute(
                "update plaza_posts set like_count = max(like_count - ?, 0) where id = ?",
                (existing_like_count, post_id),
            )
        else:
            conn.execute(
                "insert into plaza_likes (id, post_id, user_id, created_at) values (?, ?, ?, ?)",
                (like_id, post_id, user_id, iso_now()),
            )
            conn.execute("update plaza_posts set like_count = like_count + 1 where id = ?", (post_id,))
        conn.commit()
        return _row_to_post(conn, conn.execute("select * from plaza_posts where id = ?", (post_id,)).fetchone())


def increment_views(post_ids: list[str], user_id: str, event_prefix: str) -> list[PlazaPost]:
    init_plaza_store()
    if not post_ids:
        return []
    with _LOCK, _connect() as conn:
        for index, post_id in enumerate(post_ids):
            conn.execute(
                "insert into plaza_view_events (id, post_id, user_id, created_at) values (?, ?, ?, ?)",
                (f"{event_prefix}_{index}", post_id, user_id, iso_now()),
            )
            conn.execute("update plaza_posts set view_count = view_count + 1 where id = ?", (post_id,))
        conn.commit()
        placeholders = ",".join("?" for _ in post_ids)
        rows = conn.execute(f"select * from plaza_posts where id in ({placeholders})", post_ids).fetchall()
        posts_by_id = {row["id"]: _row_to_post(conn, row) for row in rows}
        return [posts_by_id[post_id] for post_id in post_ids if post_id in posts_by_id]


def _row_to_post(conn: sqlite3.Connection, row: sqlite3.Row) -> PlazaPost:
    media_rows = conn.execute(
        "select * from plaza_media where post_id = ? order by rowid asc",
        (row["id"],),
    ).fetchall()
    return PlazaPost(
        id=row["id"],
        author_id=row["author_id"],
        author_name=row["author_name"],
        icon_text=row["icon_text"],
        topic=row["topic"],
        content=row["content"],
        media_type=row["media_type"],
        media_count=row["media_count"],
        gender=row["gender"],
        verified=bool(row["verified"]),
        city=row["city"],
        age_range=row["age_range"],
        view_count=row["view_count"],
        like_count=row["like_count"],
        liked_by_current_user=bool(
            conn.execute(
                "select 1 from plaza_likes where post_id = ? and user_id = ? limit 1",
                (row["id"], user.id),
            ).fetchone()
        ),
        comment_count=row["comment_count"],
        comment_preview=row["comment_preview"],
        media=[_row_to_media(media_row) for media_row in media_rows],
        distance_text=row["distance_text"],
        created_at=row["created_at"],
    )


def _row_to_media(row: sqlite3.Row) -> PlazaMediaOut:
    return PlazaMediaOut(
        id=row["id"],
        post_id=row["post_id"],
        owner_id=row["owner_id"],
        media_type=row["media_type"],
        url=row["url"],
        storage_key=row["storage_key"],
        mime_type=row["mime_type"],
        size_bytes=row["size_bytes"],
        duration_seconds=row["duration_seconds"],
        width=row["width"],
        height=row["height"],
        created_at=row["created_at"],
    )


def _row_to_comment(row: sqlite3.Row) -> PlazaCommentOut:
    return PlazaCommentOut(
        id=row["id"],
        post_id=row["post_id"],
        author_id=row["author_id"],
        author_name=row["author_name"],
        icon_text=row["icon_text"],
        author_gender=row["author_gender"],
        author_age_range=row["author_age_range"],
        author_verified=bool(row["author_verified"]),
        author_city=row["author_city"],
        content=row["content"],
        hidden_for_owner_only=bool(row["hidden_for_owner_only"]),
        visible_to_owner_only=bool(row["visible_to_owner_only"]),
        created_at=row["created_at"],
    )
