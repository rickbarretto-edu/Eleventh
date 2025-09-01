use cursive::views::{Button, Dialog, EditView, LinearLayout, TextView};
use cursive::Cursive;
use cursive::view::Resizable;
use cursive::view::Nameable;
use super::MainMenu;

#[allow(non_snake_case)]
pub fn AccountMenu(app: &mut Cursive) {
    app.pop_layer();

    let login_button = Button::new("Login", |s| {
        let username = s
            .call_on_name("username", |view: &mut EditView| view.get_content())
            .unwrap()
            .to_string();
        let password = s
            .call_on_name("password", |view: &mut EditView| view.get_content())
            .unwrap()
            .to_string();

        let auth_result = login(&username, &password);

        match auth_result {
            Ok(auth) => {
                let auth_clone = auth.clone();
                MainMenu(s, auth_clone);
            }
            Err(err_msg) => {
                s.add_layer(Dialog::info(err_msg));
            }
        }
    });

    let signup_button = Button::new("Signup", |s| {
        let username = s
            .call_on_name("username", |view: &mut EditView| view.get_content())
            .unwrap()
            .to_string();
        let password = s
            .call_on_name("password", |view: &mut EditView| view.get_content())
            .unwrap()
            .to_string();

        let auth_result = signup(&username, &password);

        match auth_result {
            Ok(auth) => {
                let auth_clone = auth.clone();
                MainMenu(s, auth_clone);
            }
            Err(err_msg) => {
                s.add_layer(Dialog::info(err_msg));
            }
        }
    });

    let layout = LinearLayout::vertical()
        .child(TextView::new("Username"))
        .child(EditView::new().with_name("username").fixed_width(20))
        .child(TextView::new("Password"))
        .child(EditView::new().secret().with_name("password").fixed_width(20))
        .child(login_button)
        .child(signup_button);

    let dialog = Dialog::around(layout).title("Login / Signup");

    app.add_layer(dialog);
}

fn login(username: &str, password: &str) -> Result<String, String> {
    let client = reqwest::blocking::Client::new();
    let res = client
        .post("http://127.0.0.1:8080/accounts/login/")
        .json(&serde_json::json!({ "username": username, "password": password }))
        .send()
        .map_err(|_| "Failed to send request")?;

    let json: serde_json::Value = res.json().map_err(|_| "Failed to parse response")?;

    if let Some(auth) = json.get("auth").and_then(|v| v.as_str()) {
        Ok(auth.to_string())
    } else {
        Err(json.get("message")
            .and_then(|v| v.as_str())
            .map(|s| s.to_string())
            .unwrap_or_else(|| "Login failed".to_string())
        )
    }
}

fn signup(username: &str, password: &str) -> Result<String, String> {
    let client = reqwest::blocking::Client::new();
    let res = client
        .post("http://127.0.0.1:8080/accounts/create/")
        .json(&serde_json::json!({ "username": username, "password": password }))
        .send()
        .map_err(|_| "Failed to send request")?;

    let json: serde_json::Value = res.json().map_err(|_| "Failed to parse response")?;

    if let Some(auth) = json.get("auth").and_then(|v| v.as_str()) {
        Ok(auth.to_string())
    } else {
        Err(json
            .get("message")
            .and_then(|v| v.as_str())
            .unwrap_or("Signup failed").to_owned())
    }
}
