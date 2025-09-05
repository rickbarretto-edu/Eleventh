use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use rand::Rng;
use chrono::{NaiveDate, DateTime, Duration, Utc};
use tokio::time;

use crate::deck::models::Deck;
use crate::deck::repository::DailyDecks;

/// Tracks when a user last claimed a reward
#[derive(Debug, Clone)]
pub struct PlayerClaim {
    claimed_at: Option<DateTime<Utc>>,
}

/// The reward service manages daily decks and per-user rewards
#[derive(Debug, Clone)]
pub struct Rewarding {
    daily_decks: DailyDecks,
    refreshed_at: NaiveDate,
    claims: HashMap<String, PlayerClaim>,
}

impl Rewarding {
    pub fn new(mut rng: impl Rng) -> Self {
        let today = Utc::now().date_naive();
        Self {
            daily_decks: DailyDecks::new(&mut rng),
            refreshed_at: today,
            claims: HashMap::new(),
        }
    }

    pub fn shared(self) -> SharedRewarding {
        SharedRewarding::new(self)
    } 

    /// Claim a reward for a user (once per 24h).
    pub fn claim_reward(
        &mut self,
        user_id: &str,
        mut rng: impl Rng,
    ) -> Result<Deck, &'static str> {
        let now = Utc::now();
        let today = now.date_naive();

        // Refresh deck if midnight passed
        if today > self.refreshed_at {
            self.force_refresh(&mut rng);
        }

        let player_state = self.claims
            .entry(user_id.to_string())
            .or_insert(PlayerClaim { claimed_at: None });

        if let Some(last) = player_state.claimed_at {
            if now.signed_duration_since(last) < Duration::hours(24) {
                return Err("Reward already claimed in the last 24h");
            }
        }

        if let Some(deck) = self.daily_decks.reward() {
            player_state.claimed_at = Some(now);
            Ok(deck)
        } else {
            Err("No rewards available today. Try again in 24h!")
        }
    }

    /// Force deck refresh (midnight rollover).
    pub fn force_refresh(&mut self, mut rng: impl Rng) {
        self.daily_decks.regerate(&mut rng);
        self.refreshed_at = Utc::now().date_naive();
    }
}

/// Shared handle type
#[derive(Clone)]
pub struct SharedRewarding(Arc<Mutex<Rewarding>>);

impl SharedRewarding {

    pub fn new(rewarding: Rewarding) -> Self {
        SharedRewarding(Arc::new(Mutex::new(rewarding)))
    }

    fn inner(&self) -> Arc<Mutex<Rewarding>> {
        Arc::clone(&self.0)
    }

    pub fn spawn_refresher(&self) {
        let svc = self.inner();

        tokio::spawn(async move {
            loop {
                let now = Utc::now();
                let tomorrow_midnight = (now + chrono::Duration::days(1))
                    .date_naive()
                    .and_hms_opt(0, 0, 0)
                    .unwrap();
                let wait_secs = (tomorrow_midnight - now.naive_utc()).num_seconds();

                time::sleep(time::Duration::from_secs(wait_secs as u64)).await;

                if let Ok(mut svc) = svc.lock() {
                    svc.force_refresh(rand::rng());
                    println!("Decks refreshed at midnight!");
                }
            }
        });
    }

    /// Get a locked reference to mutate directly
    pub fn lock(&self) -> std::sync::MutexGuard<'_, Rewarding> {
        self.0.lock().unwrap()
    }
}

