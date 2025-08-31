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

    let local_rewards = global_rewards.clone();
    let local_inventory = global_inventories.clone();
    app.get("/user/{id}/deck/claim/", move |_req, _params| {
        let rewards = local_rewards.clone();
        let inventory = local_inventory.clone();
    
        async move {
            let mut rewards = rewards.lock();
            let mut inventories = inventory.lock();

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

    let local_inventory = global_inventories.clone();
    app.delete("/user/{id}/deck/fire/{index}", move |_req, _params| {
        let inventory = local_inventory.clone();
        async move {
            let mut inventories = inventory.lock();

            let id = _params.get("id");
            let idx = _params.get("index");
            if id.is_none() || idx.is_none() {
                return error_response("Missing user ID", vec![]);
            }

            let user_id = id.unwrap();
            let card_index = idx.unwrap().parse();

            if card_index.is_err() {
                return error_response("Bad Request, index should be a natural number.", vec![]);
            }

            let inventory = inventories.deck_of(user_id);

            match inventory.fire(card_index.unwrap()) {
                Some(_) => Response::ok().json(&json!({
                    "message": "Card removed from deck",
                })),
                None => Response::bad_request().json(&json!({
                    "message": "Could not remove from deck.",
                    "error": "index out of bounds",
                })),
            }
        }
    });

    app.get("/user/{id}/deck/", move |_req, _params| {
        let local_inventory = global_inventories.clone();
        async move {
            let mut inventories = local_inventory.lock();
            todo!()
        }
    });
}
