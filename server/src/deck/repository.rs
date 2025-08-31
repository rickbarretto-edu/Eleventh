use std::collections::HashMap;

use rand::Rng;

use super::models::Deck;
use crate::deck::models::Inventory;

#[derive(Debug, Clone)]
pub struct DailyDecks {
    decks: Vec<Deck>,
}

impl DailyDecks {
    pub fn new(mut rng: impl Rng) -> Self {
        Self {
            decks: Self::new_decks(&mut rng),
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
        (0..256).map(|_| Deck::random(&mut rng)).collect()
    }
}

use std::sync::{Arc, Mutex};


#[derive(Debug)]
pub struct Inventories {
    per_user: HashMap<String, Inventory>,
}

impl Inventories {
    pub fn new() -> Self {
        Self {
            per_user: HashMap::new(),
        }
    }

    pub fn shared(self) -> SharedInventories {
        SharedInventories::new(self)
    }

    /// Get or create an Inventory for a user
    pub fn deck_of(&mut self, user_id: &str) -> &mut Inventory {
        self.per_user.entry(user_id.into()).or_default()
    }
}

/// Shared wrapper (Arc + Mutex)
#[derive(Clone)]
pub struct SharedInventories(Arc<Mutex<Inventories>>);

impl SharedInventories {
    pub fn new(inventories: Inventories) -> Self {
        SharedInventories(Arc::new(Mutex::new(inventories)))
    }

    /// Get the inner Arc<Mutex<_>> (for cloning into tasks)
    fn inner(&self) -> Arc<Mutex<Inventories>> {
        Arc::clone(&self.0)
    }

    /// Lock and access the inventories
    pub fn lock(&self) -> std::sync::MutexGuard<'_, Inventories> {
        self.0.lock().unwrap()
    }
}
