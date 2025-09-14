use crate::services::server_url;

pub fn list(auth: &String) -> Result<reqwest::blocking::Response, reqwest::Error> {
    let client = reqwest::blocking::Client::new();
    let url: String = format!("http://{}/user/{}/deck/", server_url(), auth);
    client.get(&url).send()
}
