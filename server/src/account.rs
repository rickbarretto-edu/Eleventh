use serde_json::json;

use quickapi::response::Response;
use quickapi::server::Server;


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

        let username = _req.param("username");
        let password = _req.param("password");

        if username.is_none() || password.is_none() {
            Response::bad_request().json(&json!({
                "message": "Missing username or password",
                "links": [
                    {"rel": "back", "href": "/", "method": "GET"},
                    {"rel": "retry", "href": "/accounts/create/", "method": "POST"},
                ]
            }))
        } else {
            Response::ok().json(&json!({
                "message": "Account created successfully",
                "username": username.unwrap(),
                "links": [
                    {"rel": "self", "href": "/accounts/create", "method": "GET"},
                    {"rel": "login", "href": "/accounts/login", "method": "POST"},
                    {"rel": "home", "href": "/", "method": "GET"},
                ]
            }))
        }
    });

    app.post("/accounts/login/", |_req, _params| {

        let username = _req.param("username");
        let password = _req.param("password");

        if username.is_none() || password.is_none() {
            Response::bad_request().json(&json!({
                "message": "Missing username or password",
                "links": [
                    {"rel": "back", "href": "/", "method": "GET"},
                    {"rel": "retry", "href": "/accounts/login/", "method": "POST"},
                ]
            }))
        } else {
            Response::ok().json(&json!({
                "message": "Login successful",
                "username": username.unwrap(),
                "links": [
                    {"rel": "self", "href": "/accounts/login/", "method": "GET"},
                    {"rel": "home", "href": "/home/", "method": "GET"},
                ]
            }))
        }
    });


}