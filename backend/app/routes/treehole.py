from fastapi import APIRouter, HTTPException

from app import mock_store
from app.schemas import TreeholeCreateRequest, TreeholePostOut, TreeholeReactResponse

router = APIRouter(prefix="/treehole", tags=["treehole"])


@router.post("/posts", response_model=TreeholePostOut)
def create_treehole_post(payload: TreeholeCreateRequest) -> TreeholePostOut:
    return mock_store.create_treehole(payload.content)


@router.get("/feed", response_model=list[TreeholePostOut])
def treehole_feed() -> list[TreeholePostOut]:
    return mock_store.treeholes


@router.post("/{post_id}/react", response_model=TreeholeReactResponse)
def react_treehole(post_id: str) -> TreeholeReactResponse:
    post = mock_store.react_treehole(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="TREEHOLE_NOT_FOUND")
    return TreeholeReactResponse(status="ok", post=post)
