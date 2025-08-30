use rand::{prelude::*};
use serde::{Serialize, Deserialize};


const PLAYER_NAMES: &[&str] = &[
    "Alex", "Jordan", "Chris", "Taylor", "Morgan", "Casey", "Drew", "Jamie", "Riley", "Cameron",
    "Sam", "Lee", "Pat", "Blake", "Dakota", "Quinn", "Avery", "Emerson", "Harper", "Reese",
];
const POSITIONS: &[&str] = &["GK", "DEF", "MID", "FWD"];
const SPECIAL_CARD_NAMES: &[(&str, &str)] = &[
    ("Counter-Attack", "Launch instant play if opponent fails"),
    ("Injury", "Reduce opponent player's stats"),
    ("Super Save", "Boost GK for one turn"),
    ("Set Piece", "Free Kick/Corner with bonus"),
    ("Adrenaline Rush", "Boost stamina"),
    ("Tactical Shift", "Change formation mid-turn"),
    ("Red Card", "Remove opponent player for turn"),
    ("Dribble Mastery", "Increase attack chance"),
];


#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PlayerCard {
    pub name: String,
    pub position: String,
    pub attack: u8,
    pub defense: u8,
    pub passing: u8,
    pub stamina: u8,
}


impl PlayerCard {

    pub fn random<R: Rng>(rng: &mut R) -> Self {
        let name = PLAYER_NAMES.choose(rng)
            .unwrap_or(&"John Doe")
            .to_string();

        let position = POSITIONS.choose(rng)
            .unwrap_or(&"MID")
            .to_string();

        PlayerCard {
            name,
            position,
            attack: Self::random_stats(rng),
            defense: Self::random_stats(rng),
            passing: Self::random_stats(rng),
            stamina: Self::random_stats(rng),
        }
    }

    pub fn is(mut self, position: &str) -> Self {
        self.position = position.into();
        self
    }

    fn random_stats<R: Rng>(rng: &mut R) -> u8 {
        const MAXIMUM: u8 = 100;
        const MINIMUM: u8 = 50;
        rng.random_range(MINIMUM..=MAXIMUM)
    }

}


#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SpecialCard {
    pub name: String,
    pub effect: String,
}


impl SpecialCard {

    pub fn random<R: Rng>(rng: &mut R) -> Self {
        let (name, effect) = SPECIAL_CARD_NAMES
            .choose(rng)
            .unwrap_or(&SPECIAL_CARD_NAMES[0]);

        SpecialCard {
            name: name.to_string(),
            effect: effect.to_string(),
        }
    }

}


#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Deck {
    pub player_cards: Vec<PlayerCard>,
    pub special_cards: Vec<SpecialCard>,
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
            player_cards,
            special_cards,
        }
    }
}
