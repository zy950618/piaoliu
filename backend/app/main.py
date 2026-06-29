from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.errors import register_error_handlers
from app import db_business
from app.db import engine
from app.models import Base
from app.routes import ads, admin, bottle, checkin, dare, game, membership, me, messages, moderation, plaza, quota, relation, treehole, truth, wallet
from app.settings import get_settings

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
async def bind_user_context(request, call_next):
    client_user_id = request.headers.get("X-User-Id") or request.headers.get("X-Client-Id")
    token = db_business.set_current_user_id(client_user_id)
    try:
        return await call_next(request)
    finally:
        db_business.reset_current_user_id(token)

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
app.include_router(admin.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
