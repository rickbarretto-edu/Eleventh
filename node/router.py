from fastapi import APIRouter
from pydantic import BaseModel

from node import peers

router = APIRouter(prefix="/cluster")

class JoinRequest(BaseModel):
    peer: str
    no_spread: bool

@router.post("/join")
async def join_cluster(req: JoinRequest):
    """Add a new peer dynamically"""
    if req.peer not in peers.PEERS:
        peers.PEERS.append(req.peer)
        print(f"New peer joined: {req.peer}")
    return {"peers": peers.PEERS}

@router.get("/peers")
async def list_peers():
    return {"peers": peers.PEERS}
