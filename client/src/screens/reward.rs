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

    let res = blocking::get(&url);

    match res {
        Ok(resp) => {
            if let Ok(reward) = resp.json::<RewardResponse>() {
                if let Some(err) = reward.error {
                    let no_reward = Dialog::text(format!("{}\n{}", reward.message, err))
                        .title("Error")
                        .button("Back", move |s| MainMenu(s, auth.clone()));
                    app.add_layer(no_reward);
                } else if let Some(players) = reward.players {
                    let mut iter = players.into_iter();
                    if let Some(first) = iter.next() {
                        CardReward(app, auth.clone(), first, iter.collect());
                    }
                } else {
                    let empty_reward = Dialog::text(reward.message)
                        .title("Reward")
                        .button("Back", move |s| MainMenu(s, auth.clone()));
                    app.add_layer(empty_reward);
                }
            } else {
                let bad_response = Dialog::text("Failed to parse server response")
                    .title("Error")
                    .button("Back", move |s| MainMenu(s, auth.clone()));
                app.add_layer(bad_response);
            }
        }
        Err(e) => {
            let connection_failed = Dialog::text(format!("Request failed: {}", e))
                .title("Error")
                .button("Back", move |s| MainMenu(s, auth.clone()));
            app.add_layer(connection_failed);
        }
    }
}

#[allow(non_snake_case)]
fn CardReward(app: &mut Cursive, auth: String, player: Player, rest: Vec<Player>) {
    let info = format!(
        "{} ({})\nAttack: {}\nDefense: {}\nPassing: {}\nStamina: {}",
        player.name, player.position, player.attack, player.defense, player.passing, player.stamina
    );

    let next_button = if rest.is_empty() {
        Dialog::around(TextView::new(info))
            .title("New Player")
            .button("Finish", move |s| MainMenu(s, auth.clone()))
    } else {
        Dialog::around(TextView::new(info))
            .title("New Player")
            .button("Next", move |s| {
                let mut rest = rest.clone();
                let next = rest.remove(0);
                CardReward(s, auth.clone(), next, rest);
            })
    };

    app.pop_layer();
    app.add_layer(next_button);
}
