pub fn list(auth: &String) -> Result<reqwest::blocking::Response, reqwest::Error> {
    let client = reqwest::blocking::Client::new();
    let url: String = format!("http://server:8080/user/{}/deck/", auth);
    client.get(&url).send()
}
