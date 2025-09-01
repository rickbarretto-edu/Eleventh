use std::sync::Arc;

use cursive::views::Dialog;
use cursive::Cursive;

use super::MatchScreen;
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
            move |s| MatchScreen(s, (*auth).clone())
        })
        .button("Team", {
            let auth = auth.clone();
            move |s| TeamScreen(s, (*auth).clone())
        })
        .button("Reward", {
            let auth = auth.clone();
            move |s| RewardScreen(s, (*auth).clone())
        })
        .button("Quit", |s| s.quit());

    app.add_layer(options);
}
