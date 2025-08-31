use rand::prelude::*;
use serde::{Deserialize, Serialize};

use crate::models::cards::{PlayerCard, SpecialCard};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Deck {
    pub players: Vec<PlayerCard>,
    pub power_ups: Vec<SpecialCard>,
}

impl Deck {
    pub fn random(mut rng: impl Rng) -> Deck {
        const GOALKEEPERS: std::ops::Range<i32> = 0..1;
        const DEFENDERS: std::ops::Range<i32> = 0..4;
        const MIDFIELDERS: std::ops::Range<i32> = 0..4;
        const FORWARDS: std::ops::Range<i32> = 0..2;
        const SPECIAL_CARDS: std::ops::Range<i32> = 0..3;

        let goalkeepers: Vec<PlayerCard> = GOALKEEPERS
            .map(|_| PlayerCard::random(&mut rng).is("GK"))
            .collect();
        let defenders: Vec<PlayerCard> = DEFENDERS
            .map(|_| PlayerCard::random(&mut rng).is("DEF"))
            .collect();
        let midfielders: Vec<PlayerCard> = MIDFIELDERS
            .map(|_| PlayerCard::random(&mut rng).is("MID"))
            .collect();
        let forward: Vec<PlayerCard> = FORWARDS
            .map(|_| PlayerCard::random(&mut rng).is("FWD"))
            .collect();

        let mut player_cards: Vec<PlayerCard> = Vec::new();
        player_cards.extend(goalkeepers);
        player_cards.extend(defenders);
        player_cards.extend(midfielders);
        player_cards.extend(forward);

        let special_cards: Vec<SpecialCard> = SPECIAL_CARDS
            .map(|_| SpecialCard::random(&mut rng))
            .collect();

        Deck {
            players: player_cards,
            power_ups: special_cards,
        }
    }
}
