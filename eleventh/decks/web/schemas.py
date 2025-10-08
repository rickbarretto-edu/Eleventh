
from typing import Self, Literal
from uuid import uuid4
from pydantic import BaseModel

from eleventh.decks.model import Card as CardModel, CardID, CardID


__all__ = [
    "CardInput",
    "CardOutput",
]

class CardInput(BaseModel):
    name: str
    position: Literal['ATK', 'MID', 'DEF', 'GK']
    power: int

    def to_model(self) -> CardModel:
        return CardModel(
            id=str(uuid4()),
            name=self.name,
            position=self.position,
            power=self.power
        )
    

class CardOutput(BaseModel):
    id: CardID
    name: str
    position: Literal['ATK', 'MID', 'DEF', 'GK']
    power: int

    @classmethod
    def from_model(cls, card: CardModel) -> Self:
        return cls(
            id=card.id,
            name=card.name,
            position=card.position,
            power=card.power
        )
