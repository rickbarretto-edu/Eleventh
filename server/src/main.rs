use serde_json::json;

// QuickAPI
use quickapi::{Response, Server};

// Routes
use server::account::route_account;
use server::deck::route_decks;

// Services
use server::services::Services;
use server::services::inject;
use server::account::VirtualAccounts;
use server::deck::Inventories;
use server::deck::Rewarding;

#[tokio::main]
async fn main() {
    let rng = rand::rng();

    let services = Services {
        accounts: inject(VirtualAccounts::new()),
        inventories: inject(Inventories::new()),
        rewarding: inject(Rewarding::new(rng)),
    };

    let mut app: Server = Server::new();

    route_account(&mut app);
    route_decks(&mut app);

    app.run("127.0.0.1:8080").await;
}
