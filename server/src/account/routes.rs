use std::sync::Arc;

use serde::Deserialize;
use serde_json::json;
use quickapi::{Response, Server};

use crate::account::models::Account;

use super::repository::Accounts;

pub fn route_account(app: &mut Server) {

    let accounts = Arc::new(Accounts::at("/data/accounts.json".into()));

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
        let account = Account::new(
            data.username.clone(), 
            data.password.clone()
        );

        match accounts.store(account.clone()).await {
            Ok(_) => {
                Response::ok().json(&json!({
                    "message": "Account created successfully",
                    "username": &account.username,
                    "auth": account.auth,
                    "links": [
                        {"rel": "self", "href": "/accounts/create", "method": "GET"},
                        {"rel": "login", "href": "/accounts/login", "method": "POST"},
                        {"rel": "home", "href": "/", "method": "GET"},
                    ]
                }))
            },
            Err(e) => {
                Response::internal_error().json(&json!({
                    "message": "Failed to create account",
                    "error": e,
                }))
            }
        }
    });

    app.post("/accounts/login/", |_req, _params| async move {

        let accounts = accounts.clone();

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
        let username = data.username.clone();
        let password = data.password.clone();
        
        match accounts.by_credentials(&username, &password).await {
            Some(account) => {
                Response::ok().json(&json!({
                    "message": "Login successful",
                    "username": account.username,
                    "auth": account.auth,
                    "links": [
                        {"rel": "self", "href": "/accounts/login/", "method": "GET"},
                        {"rel": "home", "href": "/home/", "method": "GET"},
                    ]
                }))
            },
            None => Response::unauthorized().json(&json!({
                "message": "Invalid username or password",
                "links": [
                    {"rel": "retry", "href": "/accounts/login/", "method": "POST"},
                    {"rel": "create", "href": "/accounts/create/", "method": "POST"},
                ]
            })),
        }
    });
}
