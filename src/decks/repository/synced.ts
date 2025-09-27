import { Card } from "../models/cards.ts";
import { Deck } from "../models/deck.ts";
import { DecksRepository } from "./interface.ts";


export class SyncedDecks implements DecksRepository {

    from(cards: Card[]): Promise<void> {
        throw new Error("Method not implemented.")
    }

    claim(amount: number): Promise<Card[]> {
        throw new Error("Method not implemented.")
    }

    of(owner: string): Promise<Deck[]> {
        throw new Error("Method not implemented.")
    }

}