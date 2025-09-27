import { Card } from "../models/cards.ts";
import { Deck } from "../models/deck.ts";


export interface DecksRepository {

    // Create a new deck for the given owner with a standard set of cards
    from(cards: Card[]): Promise<void>

    // Claims up to `amount` cards from the shared deck
    claim(amount: number): Promise<Card[]>

    // List all decks owned by the given owner
    of(owner: string): Promise<Deck[]>
}