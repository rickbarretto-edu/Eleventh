#[cfg(test)]
extern crate speculate;
use serde_json::Value;
use server::matches::Matches;
use server::services::Services;
#[cfg(test)]
use speculate::speculate;

pub fn services() -> Services {
    use rand::rngs::StdRng;
    use rand::SeedableRng;

    use server::account::Accounts;
    use server::deck::{Inventories, Rewarding};
    use server::services::inject;

    let rng = StdRng::from_os_rng();

    Services {
        accounts: inject(Accounts::new()),
        inventories: inject(Inventories::new()),
        rewarding: inject(Rewarding::new(rng)),
        matches: inject(Matches::new()),
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
            let game: Value = serde_json::from_str(&created.body).unwrap();

            assert_eq!(created.status, 401);
            assert_eq!(game["status"], "pairing");
            assert_eq!(game["host"], "1");
        }

        it "can pair two players" {
            let _ = block_on(app.simulate("POST", "/match/1/start/", ""));
            let joined = block_on(app.simulate("POST", "/match/2/start/", ""));
            let game: Value = serde_json::from_str(&joined.body).unwrap();

            assert_eq!(game["host"], "1");
            assert_eq!(game["guest"], "2");
            assert_eq!(game["status"], "paired");
        }
        
        /// Explanation:
        /// Instead of deny the player to join the match,
        /// This behavior removes him from the latest one and migrates him
        /// to a new match.
        /// 
        /// This is not easy to test due to encapsulation, the way this was done,
        /// this logic was not exposed to the API user, working as a black-box.
        it "user can join to only one match at time" {
            let _ = block_on(app.simulate("POST", "/match/1/start/", ""));
            let not_denied = block_on(app.simulate("POST", "/match/1/start/", ""));

            assert_eq!(not_denied.status, 200);
        }
    }

    describe "Paired Match" {

        before {
            let _ = block_on(app.simulate("POST", "/match/1/start/", ""));
            let joined = block_on(app.simulate("POST", "/match/2/start/", ""));
            let game: Value = serde_json::from_str(&joined.body).unwrap();
        }

        it "status is initiated" {
            assert_eq!(game["status"], "paired");
        }
    }

}
