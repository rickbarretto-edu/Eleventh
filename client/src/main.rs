use std::sync::Arc;

use cursive::views::Dialog;
use cursive::views::LinearLayout;
use cursive::views::SelectView;
use cursive::Cursive;

use eleventh::pages::Welcome;

fn main() {
    let mut siv = cursive::default();

    Welcome::new(Arc::new(show_next)).display(&mut siv);
    siv.run();
}

fn show_next(s: &mut Cursive) {
    s.pop_layer();

    let select = SelectView::<String>::new()
        .on_submit(on_submit)
        .item("Login", String::from("Login"))
        .item("Signup", String::from("Signup"));

    s.add_layer(Dialog::around(LinearLayout::horizontal().child(select)).title("Choose an option"));
}

fn on_submit(s: &mut Cursive, item: &String) {
    s.pop_layer();
    s.add_layer(
        Dialog::text(format!("You selected: {}", item))
            .title("Selection")
            .button("Quit", |s| s.quit()),
    );
}
