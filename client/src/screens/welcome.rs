use cursive::views::Dialog;
use cursive::views::TextView;
use cursive::Cursive;

use super::AccountMenu;

#[allow(non_snake_case)]
pub fn WelcomeScreen(app: &mut Cursive) {
    let content = &vec!["Eleventh", "Only 11 win!", "", "Press <Start> to begin."];
    let body = TextView::new(content.join("\n")).center();

    let view = Dialog::around(body)
        .title("Eleventh")
        .button("Start", |s| AccountMenu(s));

    app.add_layer(view);
}
