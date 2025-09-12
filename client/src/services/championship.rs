use reqwest::blocking::Client;

use crate::schemas::championship::MatchState;
use crate::schemas::championship::Team;
use crate::services::server_url;

fn match_url(user: &str, action: &str) -> String {
    let base = format!("http://{}", server_url());
    format!("{}/match/{}/{}", base, user, action)
}

/// Join a player to a match
pub fn join(auth: &String) -> Result<String, String> {
    let client = Client::new();
    let url = match_url(auth, "start");
    let response = client.post(&url).header("Authorization", auth).send();

    match response {
        Ok(resp) => match resp.text() {
            Ok(text) => Ok(text.into()),
            Err(e) => Err(format!("Failed to read response: {}", e)),
        },
        Err(e) => Err(format!("Request error: {}", e)),
    }
}

/// Fetches the state of the current match of the player
pub fn status(auth: &String) -> Result<MatchState, String> {
    let client = Client::new();
    let url = match_url(auth, "status");
    let response = client.get(&url).send();

    match response {
        Ok(resp) => match resp.text() {
            Ok(text) => serde_json::from_str::<MatchState>(&text)
                .map_err(|e| format!("Failed to parse JSON: {}", e)),
            Err(e) => Err(format!("Failed to read response: {}", e)),
        },
        Err(e) => Err(format!("Request error: {}", e)),
    }
}

/// Name a team for a Match
pub fn name(auth: &String, team: Team) -> Result<String, String> {
    let client = Client::new();
    let url = match_url(auth, "name");
    let response = client
        .post(&url)
        .header("Authorization", auth)
        .json(&team)
        .send();

    match response {
        Ok(resp) => match resp.text() {
            Ok(text) => Ok(text),
            Err(e) => Err(format!("Failed to read response: {}", e)),
        },
        Err(e) => Err(format!("Request error: {}", e)),
    }
}
