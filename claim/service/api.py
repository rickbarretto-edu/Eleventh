from typing import Annotated

from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel

from claim.cases import claim, store, ClaimResponse, StoreResponse
from claim.token_ring import token
from claim.token_ring.model import state, Config, State


router = APIRouter()

class Card(BaseModel):
    id: str
    name: str
    power: int


def get_state() -> State:
    return state


@router.post("/setup")
async def setup(
    config: Config, 
    state: Annotated[State, Depends(get_state)]
):
    state.config = config
    print(f"[Node {config.node_id}] Configured. Next: {config.next_node}")
    return {"status": "configured", "node_id": config.node_id}


@router.post("/receive_token")
async def receive_token(
    background: BackgroundTasks, 
    state: Annotated[State, Depends(get_state)]
):
    return await token.receive_token(state, background)


@router.post("/store")
async def store_cards(
    cards: Card, 
    state: Annotated[State, Depends(get_state)]
) -> StoreResponse:
    return await store(state, cards)


@router.post("/claim")
async def claim_cards(
    state: Annotated[State, Depends(get_state)]
) -> ClaimResponse:
    """Always pops 5 cards from global deck."""
    return await claim(state, 5)


@router.get("/state")
async def get_state_info(state: Annotated[State, Depends(get_state)]):
    config = state.config
    return {
        "node_id": config.node_id if config else None,
        "has_token": config.has_token if config else None,
        "shared_list": state.shared_list,
        "queued_ops": state.pending_ops,
    }
