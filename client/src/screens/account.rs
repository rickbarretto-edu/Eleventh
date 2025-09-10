use cursive::view::Nameable;
use cursive::view::Resizable;
use cursive::views::{Button, Dialog, EditView, LinearLayout, TextView};
use cursive::Cursive;

use crate::services;
use crate::screens;

#[allow(non_snake_case)]
pub fn AccountMenu(app: &mut Cursive) {
    app.pop_layer();

    let login_button = Button::new("Login", |s| {
        let username = s
            .call_on_name("username", |view: &mut EditView| view.get_content())
            .unwrap()
            .to_string();
        let password = s
            .call_on_name("password", |view: &mut EditView| view.get_content())
            .unwrap()
            .to_string();

        let auth_result = services::account::login(&username, &password);

        match auth_result {
            Ok(auth) => {
                let auth_clone = auth.clone();
                screens::MainMenu(s, auth_clone);
            }
            Err(err_msg) => {
                s.add_layer(Dialog::info(err_msg));
            }
        }
    });

    let signup_button = Button::new("Signup", |s| {
        let username = s
            .call_on_name("username", |view: &mut EditView| view.get_content())
            .unwrap()
            .to_string();
        let password = s
            .call_on_name("password", |view: &mut EditView| view.get_content())
            .unwrap()
            .to_string();

        let auth_result = services::account::signup(&username, &password);

        match auth_result {
            Ok(auth) => {
                let auth_clone = auth.clone();
                screens::MainMenu(s, auth_clone);
            }
            Err(err_msg) => {
                s.add_layer(Dialog::info(err_msg));
            }
        }
    });

    let layout = LinearLayout::vertical()
        .child(TextView::new("Username"))
        .child(EditView::new().with_name("username").fixed_width(20))
        .child(TextView::new("Password"))
        .child(
            EditView::new()
                .secret()
                .with_name("password")
                .fixed_width(20),
        )
        .child(login_button)
        .child(signup_button);

    let dialog = Dialog::around(layout).title("Login / Signup");

    app.add_layer(dialog);
}
