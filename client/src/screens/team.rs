use cursive::views::Dialog;
use cursive::Cursive;

use super::MainMenu;

#[allow(non_snake_case)]
pub fn TeamScreen(app: &mut Cursive, auth: String) {
    app.pop_layer();

    let options = Dialog::text("Team Screen")
        .title("Team")
        .button("Back to Main", move |s| MainMenu(s, auth.clone()));

    app.add_layer(options);
}
