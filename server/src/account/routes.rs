use serde::Deserialize;
use serde_json::json;
use quickapi::{Response, Server};

use crate::account::{models::Account, repository::{Accounts, PersistentAccounts, SharedAccounts, VirtualAccounts}};

#[derive(Debug, Deserialize)]
pub struct Signup {
    pub username: String,
    pub password: String,
}

#[derive(Debug, Deserialize)]
pub struct Login {
    pub username: String,
    pub password: String,
}

/// Parse JSON body or return a bad request response
fn parse_json<T: for<'de> Deserialize<'de>>(body: &str) -> Result<T, Response> {
    serde_json::from_str(body).map_err(|_| {
        Response::bad_request().json(&json!({
            "message": "Invalid request body"
        }))
    })
}

/// Helper to build static info responses
fn route_info(message: &str, links: Vec<serde_json::Value>) -> Response {
    Response::ok().json(&json!({
        "message": message,
        "links": links
    }))
}

/// Helper for bad request with custom message + links
fn error_response(msg: &str, links: Vec<serde_json::Value>) -> Response {
    Response::bad_request().json(&json!({
        "message": msg,
        "links": links,
    }))
}

pub fn route_account(app: &mut Server) {

    let accounts = PersistentAccounts::new("/data/accounts.json").shared();

    // --- static GET routes ---

    app.get("/accounts", |_req, _params| async move {
        route_info("Account routes", vec![
            json!({"rel": "create", "href": "/accounts/create/", "method": "GET"}),
            json!({"rel": "login", "href": "/accounts/login/", "method": "GET"}),
        ])
    });

    app.get("/accounts/create/", |_req, _params| async move {
        route_info("Create Account", vec![
            json!({"rel": "self", "href": "/accounts/create/", "method": "POST"}),
            json!({"rel": "back", "href": "/accounts/", "method": "GET"}),
        ])
    });

    app.get("/accounts/login/", |_req, _params| async move {
        route_info("Enter Account", vec![
            json!({"rel": "self", "href": "/accounts/login/", "method": "POST"}),
            json!({"rel": "back", "href": "/accounts/", "method": "GET"}),
        ])
    });


    // --- dynamic POST routes ---

    let create_repo = accounts.clone();
    app.post("/accounts/create/", move |_req, _params| {
        let accounts = create_repo.clone();
        async move {
            let data: Signup = match parse_json(&_req.body) {
                Ok(d) => d,
                Err(resp) => return resp,
            };

            let account = Account::new(data.username, data.password);

            match accounts.store(account.clone()).await {
                Ok(_) => Response::ok().json(&json!({
                    "message": "Account created successfully",
                    "username": &account.username,
                    "auth": account.auth,
                    "links": [
                        {"rel": "self", "href": "/accounts/create", "method": "GET"},
                        {"rel": "login", "href": "/accounts/login", "method": "POST"},
                        {"rel": "home", "href": "/", "method": "GET"},
                    ]
                })),
                Err(e) => Response::internal_error().json(&json!({
                    "message": "Failed to create account",
                    "error": format!("{}", e),
                })),
            }
        }
    });

    let login_repo = accounts.clone();
    app.post("/accounts/login/", move |_req, _params| {
        let accounts = login_repo.clone();
        async move {
            let data: Login = match parse_json(&_req.body) {
                Ok(d) => d,
                Err(resp) => return resp,
            };

            match accounts.by_credentials(&data.username, &data.password).await {
                Some(account) => Response::ok().json(&json!({
                    "message": "Login successful",
                    "username": account.username,
                    "auth": account.auth,
                    "links": [
                        {"rel": "self", "href": "/accounts/login/", "method": "GET"},
                        {"rel": "home", "href": "/home/", "method": "GET"},
                    ]
                })),
                None => error_response("Invalid username or password", vec![
                    json!({"rel": "retry", "href": "/accounts/login/", "method": "POST"}),
                    json!({"rel": "create", "href": "/accounts/create/", "method": "POST"}),
                ]),
            }
        }
    });
}
