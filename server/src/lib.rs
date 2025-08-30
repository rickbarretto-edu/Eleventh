use quickapi::Response;
use serde::Deserialize;
use serde_json::json;

pub mod account;
pub mod menu;
pub mod deck;

/// Parse JSON body or return a bad request response
pub fn parse_json<T: for<'de> Deserialize<'de>>(body: &str) -> Result<T, Response> {
    serde_json::from_str(body).map_err(|_| {
        Response::bad_request().json(&json!({
            "message": "Invalid request body"
        }))
    })
}

/// Helper to build static info responses
pub fn route_info(message: &str, links: Vec<serde_json::Value>) -> Response {
    Response::ok().json(&json!({
        "message": message,
        "links": links
    }))
}

/// Helper for bad request with custom message + links
pub fn error_response(msg: &str, links: Vec<serde_json::Value>) -> Response {
    Response::bad_request().json(&json!({
        "message": msg,
        "links": links,
    }))
}

/// Helper for bad request with custom message + links
pub fn unauthorized_response(msg: &str, links: Vec<serde_json::Value>) -> Response {
    Response::unauthorized().json(&json!({
        "message": msg,
        "links": links,
    }))
}
