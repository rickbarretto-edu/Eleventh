use serde_json::json;

use quickapi::{Response, Server};
use server::account::route_account;
use server::account::VirtualAccounts;
use server::deck::Inventories;
use server::deck::Rewarding;
use server::menu::route_menu;
use server::deck::route_decks;
use server::services::inject;
use server::services::Services;

#[tokio::main]
async fn main() {
    let rng = rand::rng();

    let services = Services {
        accounts: inject(VirtualAccounts::new()),
        inventories: inject(Inventories::new()),
        rewarding: inject(Rewarding::new(rng)),
    };

    let mut app: Server = Server::new();

    // let accounts = Accounts::new("/data/accounts.json").shared();

    route_menu(&mut app);
    route_account(&mut app);
    route_decks(&mut app);

    // /greet?name="Rick" => Hello, Rick?
    app.route("GET", "/greet", |req, _params| async move {
        let binding: String = "Anonymous".to_string();
        let name: &String = req.param("name").unwrap_or(&binding);

        Response::ok().plain(&format!("Hello, {}!", name))
    });

    // /users/123 => {"user_id":"123"}
    app.route("GET", "/users/{id}", |_req, params| async move {
        let id: &String = params.get("id").unwrap();

        Response::ok().json(&json!({"user_id": id}))
    });

    app.run("127.0.0.1:8080").await;
}
