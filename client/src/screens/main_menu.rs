use std::sync::Arc;

use cursive::views::Dialog;
use cursive::Cursive;

use super::ChampionshipMenu;
use super::RewardScreen;
use super::TeamScreen;

#[allow(non_snake_case)]
pub fn MainMenu(app: &mut Cursive, auth: String) {
    app.pop_layer();

    let auth = Arc::new(auth);

    let options = Dialog::text("Main Menu")
        .title("Main Menu")
        .button("Match", {
            let auth = auth.clone();
            move |app| ChampionshipMenu(app, (*auth).clone())
        })
        .button("Team", {
            let auth = auth.clone();
            move |app| TeamScreen(app, (*auth).clone())
        })
        .button("Reward", {
            let auth = auth.clone();
            move |app| RewardScreen(app, (*auth).clone())
        })
        .button("Quit", |app| app.quit());

    app.add_layer(options);
}
