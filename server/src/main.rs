use std::collections::HashMap;

use serde_json::json;

use quickapi::server::Server;
use quickapi::response::Response;

#[tokio::main]
async fn main() {
    let mut app: Server = Server::new();

    // / => Welcome to Eleventh
    app.route("/", |_req, _params| 
        Response::ok().plain("Welcome to Eleventh!")
    );

    // /greet?name="Rick" => Hello, Rick?
    app.route("/greet", |req, _params| {
        let binding: String = "Anonymous".to_string();
        let name: &String = req.param("name").unwrap_or(&binding);
        
        Response::ok().plain(&format!("Hello, {}!", name))
    });

    // /users/123 => {"user_id":"123"}
    app.route("/users/{id}", |_req, params: HashMap<String, String>| {
        let id: &String = params.get("id").unwrap();
        
        Response::ok().json(&json!({"user_id": id}))
    });

    println!("Starting Eleventh app on 127.0.0.1:8080");
    app.run("127.0.0.1:8080").await;

}
