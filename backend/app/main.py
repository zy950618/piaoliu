from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.errors import register_error_handlers
from app import db_business
from app.db import engine
from app.models import Base
from app.request_context import reset_request_id, set_request_id
from app.routes import ads, admin, auth, bottle, chat, checkin, dare, game, membership, me, messages, moderation, plaza, quota, realtime, relation, rooms, treehole, truth, uploads, wallet
from app.settings import get_settings
from app.user_security import authenticate_user_token

settings = get_settings()


async def ensure_development_schema() -> None:
    if settings.environment not in {"mock", "dev", "development", "test"}:
        return
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await ensure_development_schema()
    yield


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
register_error_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=512)


@app.middleware("http")
async def bind_request_context(request: Request, call_next):
    request_id = (request.headers.get("X-Request-Id") or "").strip()[:128] or uuid4().hex
    request_id_token = set_request_id(request_id)
    authorization = request.headers.get("Authorization", "")
    user_session = None
    if authorization.startswith("Bearer "):
        user_session = authenticate_user_token(authorization.removeprefix("Bearer ").strip())
    client_user_id = user_session.user_id if user_session else request.headers.get("X-User-Id") or request.headers.get("X-Client-Id")
    public_prefixes = ("/health", "/auth/", "/admin/", "/docs", "/openapi.json")
    if settings.environment not in {"mock", "dev", "development", "test"} and not user_session and not request.url.path.startswith(public_prefixes):
        reset_request_id(request_id_token)
        return JSONResponse(
            status_code=401,
            content={
                "error": {"code": "USER_UNAUTHORIZED", "message": "登录状态已失效，请重新登录"},
                "request_id": request_id,
            },
            headers={"X-Request-Id": request_id},
        )
    token = db_business.set_current_user_id(client_user_id)
    try:
        response = await call_next(request)
        response.headers["X-Request-Id"] = request_id
        return response
    finally:
        db_business.reset_current_user_id(token)
        reset_request_id(request_id_token)

app.include_router(auth.router)
app.include_router(me.router)
app.include_router(quota.router)
app.include_router(checkin.router)
app.include_router(ads.router)
app.include_router(bottle.router)
app.include_router(truth.router)
app.include_router(dare.router)
app.include_router(game.router)
app.include_router(treehole.router)
app.include_router(membership.router)
app.include_router(moderation.router)
app.include_router(relation.router)
app.include_router(plaza.router)
app.include_router(wallet.router)
app.include_router(messages.router)
app.include_router(chat.router)
app.include_router(realtime.router)
app.include_router(rooms.router)
app.include_router(uploads.router)
app.include_router(admin.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
