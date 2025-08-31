use cursive::views::Button;
use cursive::views::Dialog;
use cursive::views::EditView;
use cursive::views::LinearLayout;
use cursive::views::TextView;
use cursive::Cursive;

use cursive::view::*;

use super::MainMenu;

#[allow(non_snake_case)]
pub fn AccountMenu(app: &mut Cursive) {
    app.pop_layer();

    let login = Button::new("Login", |s| {
        MainMenu(s);
    });

    let signup = Button::new("Signup", |s| {
        MainMenu(s);
    });

    let layout = LinearLayout::vertical()
        .child(TextView::new("Login"))
        .child(EditView::new().with_name("username").fixed_width(20))
        .child(
            EditView::new()
                .secret()
                .with_name("password")
                .fixed_width(20),
        )
        .child(login)
        .child(signup);

    let dialog = Dialog::around(layout).title("Login / Signup");

    app.add_layer(dialog);
}
