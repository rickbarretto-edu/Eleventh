from __future__ import annotations

from enum import StrEnum
import attrs

import random

FIRST_NAMES = [
    "Luca", "Marco", "Diego", "Sergio", "Pedro", "Mateo", "Lucas",
    "Carlos", "Thiago", "Rafael", "Ethan", "Noah", "Oliver", "Leo",
    "Ivan", "Mikhail", "Ander", "Hugo", "Luis", "Jonas",
]

LAST_NAMES = [
    "Silva", "Santos", "Gonzalez", "Rodriguez", "Costa", "Moreira",
    "Fernandez", "Martinez", "Nunez", "Perez", "Mendes", "Kovacs",
    "Ivanov", "Ricci", "Rossi", "Bakker", "Smith", "Brown", "Lopez",
]

class Positions(StrEnum):
    GOALKEEPER = "Goalkeeper"
    CENTER_BACK = "Center Back"
    FULLBACK = "Fullback"
    DEFENSIVE_MIDFIELDER = "Defensive Midfielder"
    CENTRAL_MIDFIELDER = "Central Midfielder"
    ATTACKING_MIDFIELDER = "Attacking Midfielder"
    WINGER = "Winger"
    FORWARD = "Forward"
    STRIKER = "Striker"


@attrs.frozen()
class Card:
    name: str
    position: Positions
    power: int

    def __str__(self) -> str:
        return f"{self.name} ({self.position} | {self.power})"
    
    @staticmethod
    def random() -> Card:
        return Card(
            name=f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            position=random.choice(list(Positions)),
            power=random.randint(50, 99)
        )