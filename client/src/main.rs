use std::sync::Arc;

use eleventh::pages::Login;
use eleventh::pages::Welcome;

fn main() {
    let mut siv = cursive::default();

    let login = Login::new();

    Welcome::new(
        Arc::new(move |app| login.clone().display(app))
    )
        .display(&mut siv);

    siv.run();
}
