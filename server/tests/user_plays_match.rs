#[cfg(test)]
extern crate speculate;
use server::matches::Matches;
use server::services::Services;
#[cfg(test)]
use speculate::speculate;

use server::models::cards::PlayerCard;

pub fn services() -> Services {
    use rand::rngs::StdRng;
    use rand::SeedableRng;

    use server::account::Accounts;
    use server::deck::{Inventories, Rewarding};
    use server::services::inject;

    let rng = String::from_os_rng();

    Services {
        accounts: inject(Accounts::new()),
        inventories: inject(Inventories::new()),
        rewarding: inject(Rewarding::new(rng)),
        matches: inject(Matches::new())
    }
}

fn block_on<F: std::future::Future>(future: F) -> F::Output {
    tokio::runtime::Runtime::new().unwrap().block_on(future)
}


speculate! {

    before {
        let mut app = quickapi::Server::new(services());
        server::matches::route_match(&mut app);
    }

    describe "Match Pairing" {
        it "starts with a host but no guest" {
            let created = block_on(app.simulate("POST", "/match/1/start/", ""));
            let game = serde_json::from_str(&created.body).unwrap();

            assert_eq!(created.status, 401);
            assert_eq!(game["status"], "pairing");
            assert_eq!(game["host"], Some("1"));
            assert_eq!(game["guest"], None);
        }

        it "can pair two players" {
            let created = block_on(app.simulate("POST", "/match/1/start/", ""));
            let joined = block_on(app.simulate("POST", "/match/2/start/", ""));
            let game = serde_json::from_str(&joined.body).unwrap();

            assert_eq!(game["host"], "1");
            assert_eq!(game["guest"], "2");
            assert_eq!(game["status"], "paired");
        }

        it "user can join to only one match at time" {
            let created = block_on(app.simulate("POST", "/match/1/start/", ""));
            let denied = block_on(app.simulate("POST", "/match/1/start/", ""));
            let game = serde_json::from_str(&joined.body).unwrap();

            assert_eq!(created.status, 502);
        }
    }

    describe "Paired Match" {

        before {
            let created = block_on(app.simulate("POST", "/match/1/start/", ""));
            let joined = block_on(app.simulate("POST", "/match/2/start/", ""));
            let game = serde_json::from_str(&joined.body).unwrap();
        }

        it "status is initiated" {
            assert_eq!(game["status"], "paired");
        }
        
        it "players can select their team" {
            assert_eq!(game["status"], "paired");

            let named = vec![
                PlayerCard::new(),
                PlayerCard::new(),
                PlayerCard::new(),
                PlayerCard::new(),
                PlayerCard::new(),
            ];
            let host = block_on(app.simulate("POST", "/match/1/name/", named.into()));
            let game = block_on(app.simulate("GET", "/match/1/status/"));
            assert_eq!(game["status"], "waiting");
            
            let guest = block_on(app.simulate("POST", "/match/2/name/", named.into()));
            let game = block_on(app.simulate("GET", "/match/2/status/"));
            
            assert_eq!(game["status"], "finished");
            assert!(game.get("score").is_some());
            assert!(game.get("winner").is_some());
        }
    }

}