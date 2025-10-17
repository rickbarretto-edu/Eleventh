from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Card(BaseModel):
    id: str
    name: str
    power: int

class Rewards(BaseModel):
    cards: list[Card]

@router.get("/")
async def get_rewards() -> Rewards:
    """Generate unique Rewards.
    
    Elects a leader, generate the cards and returns back to user.
    """
    pass