from typing import Annotated

from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel


router = APIRouter()


class Card(BaseModel):
    id: str
    name: str
    power: int


@router.post("/store")
async def store_cards(
    cards: Card, state: Annotated[State, Depends(get_state)]
) -> StoreResponse:
    return await store(state, cards)


@router.post("/claim")
async def claim_cards(state: Annotated[State, Depends(get_state)]) -> ClaimResponse:
    """Always pops 5 cards from global deck."""
    return await claim(state, 5)
