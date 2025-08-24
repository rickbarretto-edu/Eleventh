use std::collections::HashMap;

use serde_json::json;

use quickapi::server::Server;
use quickapi::response::Response;

use server::menu::route_menu;

#[tokio::main]
async fn main() {
    let mut app: Server = Server::new();

    route_menu(&mut app);

    // /greet?name="Rick" => Hello, Rick?
    app.route("GET", "/greet", |req, _params| {
        let binding: String = "Anonymous".to_string();
        let name: &String = req.param("name").unwrap_or(&binding);
        
        Response::ok().plain(&format!("Hello, {}!", name))
    });

    // /users/123 => {"user_id":"123"}
    app.route("GET", "/users/{id}", |_req, params: HashMap<String, String>| {
        let id: &String = params.get("id").unwrap();
        
        Response::ok().json(&json!({"user_id": id}))
    });

    app.run("127.0.0.1:8080").await;

}
