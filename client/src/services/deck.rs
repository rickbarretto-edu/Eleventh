

pub fn list(auth: &String) -> Result<reqwest::blocking::Response, reqwest::Error> {
    let client = reqwest::blocking::Client::new();
    let url: String = format!("http://127.0.0.1:8080/user/{}/deck/", auth);
    client.get(&url).send()
}