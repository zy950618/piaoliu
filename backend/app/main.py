from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.errors import register_error_handlers
from app.routes import ads, admin, bottle, checkin, dare, membership, me, moderation, plaza, quota, relation, treehole, truth, wallet
from app.settings import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0")
register_error_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(me.router)
app.include_router(quota.router)
app.include_router(checkin.router)
app.include_router(ads.router)
app.include_router(bottle.router)
app.include_router(truth.router)
app.include_router(dare.router)
app.include_router(treehole.router)
app.include_router(membership.router)
app.include_router(moderation.router)
app.include_router(relation.router)
app.include_router(plaza.router)
app.include_router(wallet.router)
app.include_router(admin.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
