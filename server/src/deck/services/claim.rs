use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use rand::Rng;
use chrono::{NaiveDate, DateTime, Duration, Utc};
use tokio::time;

use crate::deck::models::Deck;
use crate::deck::repository::DailyDecks;


/// Tracks when a user last claimed a reward
#[derive(Debug, Clone)]
pub struct PlayerRewardState {
    last_claimed: Option<DateTime<Utc>>,
}

/// The reward service manages daily decks and per-user rewards
#[derive(Debug)]
pub struct RewardingService {
    daily_decks: DailyDecks,
    last_deck_refresh: NaiveDate,
    players: HashMap<String, PlayerRewardState>,
}

impl RewardingService {
    pub fn new(mut rng: impl Rng) -> Self {
        let today = Utc::now().date_naive();
        Self {
            daily_decks: DailyDecks::new(&mut rng),
            last_deck_refresh: today,
            players: HashMap::new(),
        }
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
        if today > self.last_deck_refresh {
            self.force_refresh(&mut rng);
        }

        let player_state = self.players
            .entry(user_id.to_string())
            .or_insert(PlayerRewardState { last_claimed: None });

        if let Some(last) = player_state.last_claimed {
            if now.signed_duration_since(last) < Duration::hours(24) {
                return Err("Reward already claimed in the last 24h");
            }
        }

        if let Some(deck) = self.daily_decks.reward() {
            player_state.last_claimed = Some(now);
            Ok(deck)
        } else {
            Err("No rewards available today. Try again in 24h!")
        }
    }

    /// Force deck refresh (midnight rollover).
    pub fn force_refresh(&mut self, mut rng: impl Rng) {
        self.daily_decks.regerate(&mut rng);
        self.last_deck_refresh = Utc::now().date_naive();
    }

    /// Run background midnight-refresh loop.
    /// Should be spawned as a tokio task.
    pub async fn run(self: Self) {
        let service: Arc<Mutex<Self>> = Arc::new(Mutex::new(self));

        loop {
            // Compute how long until next midnight UTC
            let now = Utc::now();
            let tomorrow_midnight = (now + chrono::Duration::days(1))
                .date_naive()
                .and_hms_opt(0, 0, 0)
                .unwrap();
            let wait_secs = (tomorrow_midnight - now.naive_utc()).num_seconds();

            time::sleep(time::Duration::from_secs(wait_secs as u64)).await;

            if let Ok(mut svc) = service.lock() {
                svc.force_refresh(rand::rng());
                println!("Decks refreshed at midnight!");
            }
        }
    }
}
