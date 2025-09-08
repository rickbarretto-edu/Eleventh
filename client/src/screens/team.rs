use std::fmt::{self, Display};

use cursive::views::{Dialog, ListView, ScrollView, TextView};
use cursive::Cursive;
use reqwest::blocking::Client;
use serde::{Deserialize, Serialize};

use super::MainMenu;

#[derive(Debug, Clone)]
#[derive(Serialize, Deserialize)]
#[derive(PartialEq, Eq, Hash)]
pub struct Player {
    name: String,
    position: String,
    attack: u32,
    defense: u32,
    passing: u32,
    stamina: u32,
}

impl Display for Player {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "{} ({}) | ATK: {} | DEF: {} | PASS: {} | STA: {}",
            self.name, self.position, self.attack, self.defense, self.passing, self.stamina
        )
    }
}

#[derive(Debug, Clone)]
#[derive(Serialize, Deserialize)]
#[derive(PartialEq, Eq, Hash)]
pub struct PowerUp {
    name: String,
    effect: String,
}

impl Display for PowerUp {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}: {}", self.name, self.effect)
    }
}

#[derive(Debug, Deserialize)]
pub struct DeckResponse {
    pub players: Vec<Player>,
    pub power_ups: Vec<(PowerUp, u32)>,

    #[allow(dead_code, reason = "needed for deserialization purposes.")]
    message: String,
}

#[allow(non_snake_case)]
pub fn TeamScreen(app: &mut Cursive, auth: String) {
    app.pop_layer();

    let deck: DeckResponse = match user_deck(&auth) {
        Ok(resp) => match resp.json() {
            Ok(json) => json,
            Err(_) => {
                app.add_layer(Dialog::info("Failed to parse deck JSON"));
                return;
            }
        },
        Err(_) => {
            app.add_layer(Dialog::info("Failed to fetch deck"));
            return;
        }
    };

    let mut list = ListView::new();
    for (i, player) in deck.players.iter().enumerate() {
        let auth_clone = auth.clone();
        list.add_child("", CardItem(i, player, auth_clone));
    }

    for (_, (power, count)) in deck.power_ups.iter().enumerate() {
        list.add_child("", PowerItem(power, count));
    }

    let auth_clone = auth.clone();
    app.add_layer(
        Dialog::around(ScrollView::new(list).scroll_y(true))
            .title("Team Screen")
            .button("Back to Main", move |s| MainMenu(s, auth_clone.clone())),
    );
}

#[allow(non_snake_case)]
fn CardItem(i: usize, player: &Player, auth_clone: String) -> Dialog {
    let player_info = format!(
        "{} - {} | ATK: {} DEF: {} PASS: {} STA: {}",
        player.position, player.name, player.attack, player.defense, player.passing, player.stamina
    );

    Dialog::around(TextView::new(player_info)).button("Remove", move |s| {
        fire_player(i, &auth_clone);
        s.pop_layer();
        TeamScreen(s, auth_clone.clone());
    })
}

#[allow(non_snake_case)]
fn PowerItem(power: &PowerUp, count: &u32) -> TextView {
    let power_info = format!("{} x{} - {}", power.name, count, power.effect);
    TextView::new(power_info)
}

pub fn user_deck(auth: &String) -> Result<reqwest::blocking::Response, reqwest::Error> {
    let client = Client::new();
    let url: String = format!("http://127.0.0.1:8080/user/{}/deck/", auth);
    client.get(&url).send()
}

fn fire_player(i: usize, auth_clone: &String) {
    let url: String = format!("http://127.0.0.1:8080/user/{}/deck/fire/{}", auth_clone, i);
    let _ = Client::new().delete(&url).send();
}
