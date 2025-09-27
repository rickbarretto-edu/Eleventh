import { Card } from "./cards.ts";

export type Deck = {
    id: string
    owner: string
    cards: Card[]
}