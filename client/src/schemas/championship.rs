use serde::Deserialize;


#[derive(Deserialize)]
pub struct MatchState {
    pub status: String,
    pub host: Option<String>,
    pub guest: Option<String>,
    pub score: Option<(usize, usize)>,
    pub winner: Option<String>,
}