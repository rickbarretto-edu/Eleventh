
use rand::Rng;

use super::models::Deck;


#[derive(Debug, Clone)]
pub struct DailyDecks {
    decks: Vec<Deck>,
}


impl DailyDecks {

    pub fn new(mut rng: impl Rng) -> Self {
        Self {
            decks: Self::new_decks(&mut rng)
        }
    }

    pub fn regerate(&mut self, mut rng: impl Rng) {
        self.decks = Self::new_decks(&mut rng)
    }

    pub fn decks(self) -> Vec<Deck> {
        self.decks.clone()
    }

    pub fn reward(&mut self) -> Option<Deck> {
        self.decks.pop()
    }

    fn new_decks(mut rng: impl Rng) -> Vec<Deck> {
        (0..256)
            .map(|_| Deck::random(&mut rng))
            .collect()
    }

}


