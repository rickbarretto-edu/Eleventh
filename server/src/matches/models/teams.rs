use serde::Deserialize;
use serde::Serialize;

use crate::models::cards::PlayerCard;
use crate::models::cards::SpecialCard;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Team {
    named: Vec<PlayerCard>,
    helper: SpecialCard,
}

impl Team {
    pub fn play_with(&self, other: &Team) -> (usize, usize) {
        (1, 0)
    }
}
