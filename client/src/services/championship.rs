use reqwest::blocking::Client;

/// Join a player to a match
pub fn join(auth: &String) -> Result<String, String> {
    let client = Client::new();
    let url = format!("http://127.0.0.1:8080/match/{}/start/", auth);

    let response = client
        .post(&url)
        .header("Authorization", auth)
        .send();

    match response {
        Ok(resp) => match resp.text() {
            Ok(text) => Ok(text.into()),
            Err(e) => Err(format!("Failed to read response: {}", e)),
        },
        Err(e) => Err(format!("Request error: {}", e)),
    }
} 