use cursive::views::Dialog;
use cursive::Cursive;

use super::MainMenu;

#[allow(non_snake_case)]
pub fn MatchScreen(app: &mut Cursive) {
    app.pop_layer();

    let options = Dialog::text("Match Screen")
        .title("Match")
        .button("Back to Main", |s| MainMenu(s));

    app.add_layer(options);
}
