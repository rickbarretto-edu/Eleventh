use cursive::views::Dialog;
use cursive::Cursive;

use super::MatchScreen;
use super::RewardScreen;
use super::TeamScreen;

#[allow(non_snake_case)]
pub fn MainMenu(app: &mut Cursive) {
    app.pop_layer();

    let options = Dialog::text("Main Menu")
        .title("Main Menu")
        .button("Match", |s| MatchScreen(s))
        .button("Team", |s| TeamScreen(s))
        .button("Reward", |s| RewardScreen(s))
        .button("Quit", |s| s.quit());

    app.add_layer(options);
}
