from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from eleventh.decks.model import Card, CardID, UserID
from eleventh.decks.repo import InMemoryDecks
from eleventh.decks.web.schemas import CardInput, CardOutput


_decks_instance = InMemoryDecks()

def get_decks() -> InMemoryDecks:
    return _decks_instance


route = APIRouter(prefix="/api", tags=["decks"])


class SellCardRequest(BaseModel):
    card: CardID


@route.get("/deck/{user_id}")
async def get_user_deck(
    user_id: UserID, 
    decks: Annotated[InMemoryDecks, Depends(get_decks)]
) -> list[CardOutput]:
    cards = await decks.owned_by(user_id)
    return [CardOutput.from_model(card) for card in cards]


@route.post("/deck/add/{user_id}")
async def add_cards(
    user_id: UserID, 
    cards: list[CardInput],
    decks: Annotated[InMemoryDecks, Depends(get_decks)]
) -> None:
    """Add cards to the user's deck.
    
    Curl Usage
    ----------

            curl -X POST "http://localhost:8000/api/deck/add/rick" -H "Content-Type: application/json" -d '[{"name": "Cristiano Ronaldo", "position": "ATK", "power": 95}]'
            curl -X POST "http://localhost:8000/api/deck/add/rick" -H "Content-Type: application/json" -d '[{"name": "Lionel Messi", "position": "ATK", "power": 93}, {"name": "Luka Modric", "position": "MID", "power": 87}, {"name": "Sergio Ramos", "position": "DEF", "power": 88}, {"name": "Manuel Neuer", "position": "GK", "power": 90}]'
    """
    card_models = [card.to_model() for card in cards]
    await decks.add_cards(user_id, card_models)


@route.post("/deck/{user_id}/sell")
async def sell_cards(
    user_id: UserID, 
    payload: SellCardRequest,
    decks: Annotated[InMemoryDecks, Depends(get_decks)]
) -> None:
    await decks.remove_card(user_id, payload.card)
