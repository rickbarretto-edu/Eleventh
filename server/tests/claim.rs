
use quickapi::server::Server;
use server::deck::route_decks;
use server::services::Services;
use speculate::speculate;

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


fn block_on<F: std::future::Future>(future: F) -> F::Output {
    tokio::runtime::Runtime::new().unwrap().block_on(future)
}

speculate! {

    describe "User Claims Deck" {

        before {
            let mut app = Server::new(services());
            route_decks(&mut app);
        }

        it "should get a new deck" {
            let response = block_on(app.simulate("GET", "/user/123/deck/claim/", ""));
            assert_eq!(response.status, 200);

            let body: serde_json::Value = serde_json::from_str(&response.body).unwrap();
            assert_eq!(body["message"], "You got new cards!");
            assert!(body["players"].is_array());
            assert!(body["power_ups"].is_array());
        }

        it "should prevent claiming twice in 24h" {
                // first claim
            let _ = block_on(app.simulate("GET", "/user/123/deck/claim/", ""));

            // second claim
            let second = block_on(app.simulate("GET", "/user/123/deck/claim", ""));
            assert_eq!(second.status, 400);

            let body: serde_json::Value = serde_json::from_str(&second.body).unwrap();
            assert_eq!(body["message"], "Could not claim reward!");
            assert_eq!(body["error"], "Reward already claimed in the last 24h");
        }
    }
}
