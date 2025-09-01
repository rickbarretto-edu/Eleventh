use cursive::views::{Dialog, TextView};
use cursive::Cursive;
use reqwest::blocking;
use serde::Deserialize;

use super::MainMenu;

#[derive(Debug, Clone, Deserialize)]
struct Player {
    name: String,
    position: String,
    attack: u32,
    defense: u32,
    passing: u32,
    stamina: u32,
}

#[derive(Debug, Clone, Deserialize)]
struct PowerUp {
    name: String,
    effect: String,
}

#[derive(Debug, Deserialize)]
struct RewardResponse {
    message: String,
    players: Option<Vec<Player>>,
    power_ups: Option<Vec<(PowerUp, u32)>>,
    error: Option<String>,
}

#[allow(non_snake_case)]
pub fn RewardScreen(app: &mut Cursive, auth: String) {
    app.pop_layer();

    let url = format!("http://127.0.0.1:8080/user/{}/deck/claim", auth);
    let response = blocking::get(&url);

    if response.is_err() {
        return ErrorDialog(app, auth, format!("Request failed: {}", e));
    }

    if let Ok(reward) = response.unwrap().json::<RewardResponse>() {
        if let Some(err) = reward.error {
            ErrorDialog(app, auth, format!("{}\n{}", reward.message, err));
        } else if let Some(players) = reward.players {
            let mut iter = players.into_iter();
            if let Some(first) = iter.next() {
                EarnedCard(app, auth.clone(), first, iter.collect());
            }
        } else {
            InfoDialog(app, auth, "Reward", reward.message);
        }
    } else {
        ErrorDialog(app, auth, "Failed to parse server response".into());
    }
}

#[allow(non_snake_case)]
fn EarnedCard(app: &mut Cursive, auth: String, player: Player, rest: Vec<Player>) {
    let info = format!(
        "{} ({})\nAttack: {}\nDefense: {}\nPassing: {}\nStamina: {}",
        player.name, player.position, player.attack, player.defense, player.passing, player.stamina
    );

    let dialog = Dialog::around(TextView::new(info))
        .title("New Player");

    let next_button = if rest.is_empty() {
        dialog.button("Finish", move |s| {
            MainMenu(s, auth.clone())
        })
    } else {
        dialog.button("Next", move |s| {
            let mut rest = rest.clone();
            let next = rest.remove(0);
            EarnedCard(s, auth.clone(), next, rest);
        })
    };

    app.pop_layer();
    app.add_layer(next_button);
}

#[allow(non_snake_case)]
fn ErrorDialog(app: &mut Cursive, auth: String, msg: String) {
    let dialog = Dialog::text(msg)
        .title("Error")
        .button("Back", move |s| MainMenu(s, auth.clone()));
    app.add_layer(dialog);
}

#[allow(non_snake_case)]
fn InfoDialog(app: &mut Cursive, auth: String, title: &str, msg: String) {
    let dialog = Dialog::text(msg)
        .title(title)
        .button("Back", move |s| MainMenu(s, auth.clone()));
    app.add_layer(dialog);
}