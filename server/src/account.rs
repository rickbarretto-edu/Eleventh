use std::collections::HashMap;
use std::fs;
use std::path::PathBuf;
use std::time::{SystemTime, UNIX_EPOCH};

use serde::{Deserialize, Serialize};
use serde_json::json;
use uuid::Uuid;

use quickapi::{Server, Response};


#[derive(Serialize, Deserialize, Debug)]
struct Account {
    username: String,
    password: String,
    created_at: String,
    auth: String
}

type Accounts = HashMap<String, Account>;

fn db_path() -> PathBuf {
    // Use the crate manifest dir so the path is predictable at runtime.
    PathBuf::from(concat!(env!("CARGO_MANIFEST_DIR"), "/data/accounts.json"))
}

fn load_accounts() -> Result<Accounts, String> {
    let path = db_path();

    if !path.exists() {
        return Ok(HashMap::new());
    }

    let s = fs::read_to_string(&path).map_err(|e| format!("failed to read DB file: {}", e))?;
    let map: Accounts = serde_json::from_str(&s).map_err(|e| format!("invalid DB JSON: {}", e))?;
    Ok(map)
}

fn save_accounts(accounts: &Accounts) -> Result<(), String> {
    let path = db_path();
    let serialized = serde_json::to_string_pretty(accounts).map_err(|e| format!("serialize error: {}", e))?;
    fs::write(&path, serialized).map_err(|e| format!("failed to write DB file: {}", e))
}

pub fn route_account(app: &mut Server) {

    app.get("/accounts", |_req, _params| 
        Response::ok().json(&json!({
            "message": "Account routes",
            "links": [
                {"rel": "create", "href": "/accounts/create/", "method": "GET"},
                {"rel": "login", "href": "/accounts/login/", "method": "GET"},
            ]
        }))
    );

    app.get("/accounts/create/", |_req, _params| 
        Response::ok().json(&json!({
            "message": "Create Account",
            "requires": ["username", "password"],
            "links": [
                {"rel": "self", "href": "/accounts/create/", "method": "POST"},
                {"rel": "back", "href": "/accounts/", "method": "GET"},
            ]
        }))
    );

    app.get("/accounts/login/", |_req, _params| 
        Response::ok().json(&json!({
            "message": "Enter Account",
            "requires": ["username", "password"],
            "links": [
                {"rel": "self", "href": "/accounts/login/", "method": "POST"},
                {"rel": "back", "href": "/accounts/", "method": "GET"},
            ]
        }))
    );

    app.post("/accounts/create/", |_req, _params| {

        #[derive(Debug, Deserialize)]
        struct Signup {
            pub username: String,
            pub password: String,
        }

        let data: Result<Signup, serde_json::Error> = serde_json::from_str(&_req.body);

        if data.is_err() {
            return Response::bad_request().json(&json!({
                "message": "Missing username or password",
                "links": [
                    {"rel": "back", "href": "/", "method": "GET"},
                    {"rel": "retry", "href": "/accounts/create/", "method": "POST"},
                ]
            }));
        }

        let data = data.unwrap();
        let username: String = data.username.into();
        let password: String = data.password.into();

        match load_accounts() {
            Ok(mut accounts) => {
                if accounts.contains_key(&username) {
                    return Response::bad_request().json(&json!({
                        "message": "Username already exists",
                        "links": [
                            {"rel": "back", "href": "/accounts/create/", "method": "GET"},
                        ]
                    }));
                }

                let created_at = SystemTime::now().duration_since(UNIX_EPOCH)
                    .map(|d| d.as_secs().to_string()).unwrap_or_else(|_| "0".to_string());

                let auth = Uuid::new_v4().to_string();
                let acct = Account { username: username.clone(), password: password.clone(), created_at, auth: auth.clone() };
                accounts.insert(username.clone(), acct);

                if let Err(e) = save_accounts(&accounts) {
                    return Response::internal_error().json(&json!({
                        "message": "Failed to save account",
                        "error": e,
                    }));
                }

                Response::ok().json(&json!({
                    "message": "Account created successfully",
                    "username": username,
                    "auth": auth,
                    "links": [
                        {"rel": "self", "href": "/accounts/create", "method": "GET"},
                        {"rel": "login", "href": "/accounts/login", "method": "POST"},
                        {"rel": "home", "href": "/", "method": "GET"},
                    ]
                }))
            }
            Err(e) => Response::internal_error().json(&json!({
                "message": "Failed to read accounts DB",
                "error": e,
            }))
        }
    });

    app.post("/accounts/login/", |_req, _params| {

        #[derive(Debug, Deserialize)]
        struct Login {
            pub username: String,
            pub password: String,
        }

        let data: Result<Login, serde_json::Error> = serde_json::from_str(&_req.body);

        if data.is_err() {
            return Response::bad_request().json(&json!({
                "message": "Missing username or password",
                "links": [
                    {"rel": "back", "href": "/", "method": "GET"},
                    {"rel": "retry", "href": "/accounts/login/", "method": "POST"},
                ]
            }));
        }

        let data = data.unwrap();
        let username: String = data.username.into();
        let password: String = data.password.into();

        match load_accounts() {
            Ok(accounts) => {
                match accounts.get(&username) {
                    Some(account) if account.password == *password => {
                        Response::ok().json(&json!({
                            "message": "Login successful",
                            "username": account.username,
                            "auth": account.auth,
                            "links": [
                                {"rel": "self", "href": "/accounts/login/", "method": "GET"},
                                {"rel": "home", "href": "/home/", "method": "GET"},
                            ]
                        }))
                    }
                    _ => Response::unauthorized().json(&json!({
                        "message": "Invalid username or password",
                        "links": [
                            {"rel": "retry", "href": "/accounts/login/", "method": "POST"},
                            {"rel": "create", "href": "/accounts/create/", "method": "POST"},
                        ]
                    })),
                }
            }
            Err(e) => Response::internal_error().json(&json!({
                "message": "Failed to read accounts DB",
                "error": e,
            }))
        }
    });

}