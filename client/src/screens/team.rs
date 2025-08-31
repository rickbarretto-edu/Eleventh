use cursive::views::Dialog;
use cursive::Cursive;

use super::MainMenu;

#[allow(non_snake_case)]
pub fn TeamScreen(app: &mut Cursive) {
    app.pop_layer();

    let options = Dialog::text("Team Screen")
        .title("Team")
        .button("Back to Main", |s| MainMenu(s));

    app.add_layer(options);
}
