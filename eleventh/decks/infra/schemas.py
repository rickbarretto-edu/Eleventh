
from typing import Self, Literal
from pydantic import BaseModel

from eleventh.decks.model import Card as CardModel, CardID


class Card(BaseModel):
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

    def to_model(self) -> CardModel:
        return CardModel(
            id=self.id,
            name=self.name,
            position=self.position,
            power=self.power
        )