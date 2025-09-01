use cursive::views::Dialog;
use cursive::Cursive;

use super::MainMenu;

#[allow(non_snake_case)]
pub fn MatchScreen(app: &mut Cursive, auth: String) {
    app.pop_layer();

    let options = Dialog::text("Match Screen")
        .title("Match")
        .button("Back to Main", move |s| MainMenu(s, auth.clone()));

    app.add_layer(options);
}
