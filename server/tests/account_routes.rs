#[cfg(test)]
extern crate speculate;

#[cfg(test)]
use speculate::speculate;

use std::fs;
use std::path::PathBuf;

use serde_json::json;

use quickapi::server::{Response, Server};
use server::account::route_account;
use server::services::Services;

fn block_on<F: std::future::Future>(future: F) -> F::Output {
    tokio::runtime::Runtime::new().unwrap().block_on(future)
}

pub fn services() -> Services {
    use server::services::inject;
    use server::account::VirtualAccounts;
    use server::deck::{Inventories, Rewarding};

    Services {
        accounts: inject(VirtualAccounts::new()),
        inventories: inject(Inventories::new()),
        rewarding: inject(Rewarding::new(rand::rng())),
    }
}

/// Clean database to make sure tests are independent
///
/// Be careful with race conditions if tests are run in parallel.
fn cleanup_db() {
    let path = PathBuf::from(concat!(env!("CARGO_MANIFEST_DIR"), "/data/accounts.json"));
    let _ = fs::remove_file(path);
}

speculate! {

    describe "Accounts Route" {

        before {
            let mut app = Server::new(services());
            route_account(&mut app);
        }

        it "has main route" {
            let response: Response = block_on(app.simulate("GET", "/accounts", ""));
            assert_eq!(response.status, 200);

            let body: serde_json::Value = serde_json::from_str(&response.body).unwrap();
            assert_eq!(body["message"], "Account routes");
        }

        it "creates account" {
            let payload = json!({
                "username": "alice",
                "password": "secret"
            }).to_string();

            let res = block_on(app.simulate("POST", "/accounts/create/", &payload));
            assert_eq!(res.status, 200);

            let body: serde_json::Value = serde_json::from_str(&res.body).unwrap();
            assert_eq!(body["message"], "Account created successfully");
            assert_eq!(body["username"], "alice");
            assert!(body.get("auth").is_some());
        }

        it "doesn't duplicate" {
            let payload = json!({
                "username": "bob",
                "password": "secret"
            }).to_string();

            let create_new = block_on(app.simulate("POST", "/accounts/create/", &payload));
            assert_eq!(create_new.status, 200);

            let recreate = block_on(app.simulate("POST", "/accounts/create/", &payload));
            assert_eq!(recreate.status, 400);

            let body: serde_json::Value = serde_json::from_str(&recreate.body).unwrap();
            assert_eq!(body["message"], "Username already exists");
        }

        it "can't register for invalid body" {
            let response = block_on(app.simulate("POST", "/accounts/create/", "not-json"));
            assert_eq!(response.status, 400);

            let body: serde_json::Value = serde_json::from_str(&response.body).unwrap();
            assert_eq!(body["message"], "Invalid request body");
        }
    }

    describe "New user Charlie" {

        before {
            let mut app = Server::new(services());
            route_account(&mut app);
        }

        after {
            cleanup_db();
        }

        it "creates a new account" {
            let signup = json!({
                "username": "charlie",
                "password": "12345"
            }).to_string();

            let response = block_on(app.simulate("POST", "/accounts/create/", &signup));
            assert_eq!(response.status, 200);
        }

        it "insert wrong credentials" {
            block_on(
                app.simulate("POST", "/accounts/create/", &json!({
                    "username": "charlie",
                    "password": "right"
                }).to_string())
            );

            let wrong_login = json!({
                "username": "charlie",
                "password": "wrong"
            }).to_string();

            let response = block_on(app.simulate("POST", "/accounts/login/", &wrong_login));
            assert_eq!(response.status, 401);

            let body: serde_json::Value = serde_json::from_str(&response.body).unwrap();
            assert_eq!(body["message"], "Invalid username or password");
        }

        it "insert correct credentials" {
            block_on(
                app.simulate("POST", "/accounts/create/", &json!({
                    "username": "charlie",
                    "password": "right"
                }).to_string())
            );

            let login = json!({
                "username": "charlie",
                "password": "right"
            }).to_string();

            let response = block_on(app.simulate("POST", "/accounts/login/", &login));
            assert_eq!(response.status, 200);

            let body: serde_json::Value = serde_json::from_str(&response.body).unwrap();
            assert_eq!(body["message"], "Login successful");
            assert_eq!(body["username"], "charlie");
        }
    }
}
