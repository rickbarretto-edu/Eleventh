use cursive::views::Dialog;
use cursive::views::TextView;
use cursive::Cursive;

use super::AccountMenu;

#[allow(non_snake_case)]
pub fn Welcome(app: &mut Cursive) {
    let content = &vec!["Eleventh", "Only 11 win!", "", "Press <Start> to begin."];
    let body = TextView::new(content.join("\n")).center();

    let view = Dialog::around(body)
        .title("Eleventh")
        .button("Start", |app| AccountMenu(app));

    app.add_layer(view);
}
