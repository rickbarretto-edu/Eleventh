use serde::Deserialize;
use serde_json::json;

use quickapi::{Response, Server};

use super::repository::DailyDecks;
use super::repository::Inventories;
use crate::{error_response, parse_json, route_info, unauthorized_response};

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
    let daily_decks = DailyDecks::new(rand::rng());
    let inventories = Inventories::new();


    let daily_decks = daily_decks.clone();
    let inventories_repo = inventories.clone();
    app.get("/user/{id}/deck/claim/", move |_req, _params| {
        let daily_decks = daily_decks.clone();
        let inventories = inventories_repo.clone();
        async move {

            todo!()
        }
    });

    let inventories_repo = inventories.clone();
    app.delete("/user/deck/fire/{index}", move |_req, _params| {
        let inventories = inventories_repo.clone();
        async move {

          todo!()
        }
    });

    let inventories_repo = inventories.clone();
    app.get("/user/{id}/deck/", move |_req, _params| {
        let inventories = inventories_repo.clone();
        async move {

          todo!()
        }
    });

}
