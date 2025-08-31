use serde::Deserialize;
use serde_json::json;

use quickapi::{Response, Server};

use super::repository::Inventories;
use super::services::claim::Rewarding;
use crate::error_response;

#[derive(Debug, Deserialize)]
pub struct ClaimBody {
    pub auth: String,
}

#[derive(Debug, Deserialize)]
pub struct Login {
    pub username: String,
    pub password: String,
}

pub fn route_decks(app: &mut Server) {
    let global_rewards = Rewarding::new(rand::rng()).shared();
    let global_inventories = Inventories::new().shared();

    global_rewards.spawn_refresher();


    app.get("/user/{id}/deck/claim/", move |_req, _params| {
        let local_rewards = global_rewards.clone();
        let local_inventory = global_inventories.clone();
        async move {

            let mut rewards = local_rewards.lock();
            let mut inventories = local_inventory.lock();

            let id = _params.get("id");

            if id.is_none() {
                return error_response("Missing user ID", vec![]);
            }

            let user_id = id.unwrap();
            match rewards.claim_reward(user_id, rand::rng()) {
                Err(e) => Response::bad_request().json(&json!({
                    "message": "Could not claim reward!",
                    "error": e,
                })),
                Ok(claimed) => {
                    let inventory = inventories.deck_of(user_id);
                    inventory.add_deck(claimed);

                    Response::ok().json(&json!({
                        "message": "You got new cards!",
                        "players": inventory.clone().players(),
                        "power_ups": inventory.clone().power_ups(),
                    }))
                }
            }
        }
    });

    app.delete("/user/deck/fire/{index}", move |_req, _params| {
        async move {

          todo!()
        }
    });

    app.get("/user/{id}/deck/", move |_req, _params| {
        async move {

          todo!()
        }
    });

}
