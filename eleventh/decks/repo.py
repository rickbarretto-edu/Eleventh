


import attrs

from eleventh.decks.model import CardID, UserID
from eleventh.decks.model import Card

@attrs.frozen
class InMemoryDecks:
    database: dict[UserID, dict[CardID, Card]] = attrs.field(factory=dict)

    async def owned_by(self, owner_id: UserID) -> list[Card]:
        return list(self.database.get(owner_id, {}).values())

    async def add_cards(self, owner_id: UserID, cards: list[Card]) -> None:
        if owner_id not in self.database:
            self.database[owner_id] = {}
        for card in cards:
            self.database[owner_id][card.id] = card

    async def remove_card(self, owner_id: UserID, card_id: CardID) -> None:
        if owner_id in self.database:
            self.database[owner_id].pop(card_id, None)
