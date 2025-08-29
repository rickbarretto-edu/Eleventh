use serde::Deserialize;
use serde_json::json;
use quickapi::{Response, Server};

use super::repository::{load_accounts, save_accounts, new_account};

pub fn route_account(app: &mut Server) {
    app.get("/accounts", |_req, _params| async move {
        Response::ok().json(&json!({
            "message": "Account routes",
            "links": [
                {"rel": "create", "href": "/accounts/create/", "method": "GET"},
                {"rel": "login", "href": "/accounts/login/", "method": "GET"},
            ]
        }))
    });

    app.get("/accounts/create/", |_req, _params| async move {
        Response::ok().json(&json!({
            "message": "Create Account",
            "requires": ["username", "password"],
            "links": [
                {"rel": "self", "href": "/accounts/create/", "method": "POST"},
                {"rel": "back", "href": "/accounts/", "method": "GET"},
            ]
        }))
    });

    app.get("/accounts/login/", |_req, _params| async move {
        Response::ok().json(&json!({
            "message": "Enter Account",
            "requires": ["username", "password"],
            "links": [
                {"rel": "self", "href": "/accounts/login/", "method": "POST"},
                {"rel": "back", "href": "/accounts/", "method": "GET"},
            ]
        }))
    });

    app.post("/accounts/create/", |_req, _params| async move {
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
        match load_accounts().await {
            Ok(mut accounts) => {
                if accounts.contains_key(&data.username) {
                    return Response::bad_request().json(&json!({
                        "message": "Username already exists",
                        "links": [
                            {"rel": "back", "href": "/accounts/create/", "method": "GET"},
                        ]
                    }));
                }

                let acct = new_account(data.username.clone(), data.password.clone());
                accounts.insert(data.username.clone(), acct.clone());

                if let Err(e) = save_accounts(&accounts).await {
                    return Response::internal_error().json(&json!({
                        "message": "Failed to save account",
                        "error": e,
                    }));
                }

                Response::ok().json(&json!({
                    "message": "Account created successfully",
                    "username": acct.username,
                    "auth": acct.auth,
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
            })),
        }
    });

    app.post("/accounts/login/", |_req, _params| async move {
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
        match load_accounts().await {
            Ok(accounts) => match accounts.get(&data.username) {
                Some(account) if account.password == data.password => {
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
            },
            Err(e) => Response::internal_error().json(&json!({
                "message": "Failed to read accounts DB",
                "error": e,
            })),
        }
    });
}
