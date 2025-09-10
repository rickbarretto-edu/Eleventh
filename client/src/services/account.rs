

pub fn signup(username: &str, password: &str) -> Result<String, String> {
    let url = "http://127.0.0.1:8080/accounts/create/";
    let res = request_at(url, username, password)?;
    let json = humanized_result(res)?;
    auth_or_error(json, "Signup failed")
}

pub fn login(username: &str, password: &str) -> Result<String, String> {
    let url = "http://127.0.0.1:8080/accounts/login/";
    let res = request_at(username, password, url)?;
    let json = humanized_result(res)?;
    auth_or_error(json, "Login failed")
}

fn request_at(username: &str, password: &str, url: &str) -> Result<reqwest::blocking::Response, String> {
    let client = reqwest::blocking::Client::new();
    let res = client
        .post(url)
        .json(&serde_json::json!({ "username": username, "password": password }))
        .send()
        .map_err(|_| "Failed to send request")?;
    Ok(res)
}

fn humanized_result(res: reqwest::blocking::Response) -> Result<serde_json::Value, String> {
    let json: serde_json::Value = res.json().map_err(|_| "Failed to parse response")?;
    Ok(json)
}

fn auth_or_error(json: serde_json::Value, error_message: &'static str) -> Result<String, String> {
    match json.get("auth").and_then(|v| v.as_str()) {
        Some(auth) => Ok(auth.to_string()),
        None => {
            Err(json
                .get("message")
                .and_then(|v| v.as_str())
                .unwrap_or(error_message)
                .to_owned())
        }
    }
}