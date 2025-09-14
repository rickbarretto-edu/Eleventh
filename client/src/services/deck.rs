use reqwest::blocking::Client;

use crate::services::server_url;

fn deck_url(user: &str, action: &str) -> String {
    format!("http://{}/user/{}/deck/{}", server_url(), user, action)
}

pub fn list(auth: &String) -> Result<reqwest::blocking::Response, reqwest::Error> {
    let client = Client::new();
    let url = deck_url("", auth);
    client.get(&url).send()
}

pub fn fire_player(i: usize, auth_clone: &String) {
    let url = deck_url(&auth_clone, &format!("fire/{}", i));
    let _ = Client::new().delete(&url).send();
}