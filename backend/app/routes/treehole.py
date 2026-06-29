from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import db_business
from app.db import get_db_session
from app.schemas import TreeholeCreateRequest, TreeholePostOut, TreeholeReactResponse

router = APIRouter(prefix="/treehole", tags=["treehole"])


@router.post("/posts", response_model=TreeholePostOut)
async def create_treehole_post(payload: TreeholeCreateRequest, session: AsyncSession = Depends(get_db_session)) -> TreeholePostOut:
    return await db_business.create_treehole(session, payload.content)


@router.get("/feed", response_model=list[TreeholePostOut])
async def treehole_feed(session: AsyncSession = Depends(get_db_session)) -> list[TreeholePostOut]:
    return await db_business.treehole_feed(session)


@router.post("/{post_id}/react", response_model=TreeholeReactResponse)
async def react_treehole(post_id: str, session: AsyncSession = Depends(get_db_session)) -> TreeholeReactResponse:
    return TreeholeReactResponse(status="ok", post=await db_business.react_treehole(session, post_id))


@router.post("/{post_id}/reply", response_model=TreeholeReactResponse)
async def reply_treehole(post_id: str, payload: TreeholeCreateRequest, session: AsyncSession = Depends(get_db_session)) -> TreeholeReactResponse:
    return TreeholeReactResponse(status="ok", post=await db_business.reply_treehole(session, post_id, payload.content))
