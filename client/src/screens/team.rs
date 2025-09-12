use cursive::views::{Dialog, ListView, ScrollView, TextView};
use cursive::Cursive;
use reqwest::blocking::Client;

use crate::schemas::deck::DeckResponse;
use crate::schemas::deck::Player;
use crate::schemas::deck::PowerUp;
use crate::services::server_url;
use crate::{screens, services};

#[allow(non_snake_case)]
pub fn TeamScreen(app: &mut Cursive, auth: String) {
    app.pop_layer();

    let deck = match deck_of(app, &auth) {
        Some(value) => value,
        None => return,
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
            .button("Back to Main", move |s| {
                screens::MainMenu(s, auth_clone.clone())
            }),
    );
}

fn deck_of(app: &mut Cursive, auth: &String) -> Option<DeckResponse> {
    let deck: DeckResponse = match services::deck::list(auth) {
        Ok(resp) => match resp.json() {
            Ok(json) => json,
            Err(_) => {
                app.add_layer(Dialog::info("Failed to parse deck JSON"));
                return None;
            }
        },
        Err(_) => {
            app.add_layer(Dialog::info("Failed to fetch deck"));
            return None;
        }
    };
    Some(deck)
}

#[allow(non_snake_case)]
fn CardItem(i: usize, player: &Player, auth_clone: String) -> Dialog {
    let player_info = format!("{}", player);

    Dialog::around(TextView::new(player_info)).button("Remove", move |s| {
        fire_player(i, &auth_clone);
        s.pop_layer();
        TeamScreen(s, auth_clone.clone());
    })
}

#[allow(non_snake_case)]
fn PowerItem(power: &PowerUp, count: &u32) -> TextView {
    let power_info = format!("{}x : {}", count, power);
    TextView::new(power_info)
}

fn fire_url(user: &str, index: usize) -> String {
    let base = format!("http://{}/", server_url());
    format!("{}/user/{}/deck/fire/{}", base, user, index)
}

fn fire_player(i: usize, auth_clone: &String) {
    let url = fire_url(&auth_clone, i);
    let _ = Client::new().delete(&url).send();
}
