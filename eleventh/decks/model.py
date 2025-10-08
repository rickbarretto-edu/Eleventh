

from typing import Literal
from uuid import UUID, uuid4
import attrs

type CardID = str
type UserID = str

def new_card_id() -> CardID:
    return "card-" + str(uuid4())

@attrs.frozen
class Card:
    name: str
    position: Literal["ATK", "MID", "DEF", "GK"]
    power: int
    id: CardID = attrs.field(factory=new_card_id)

