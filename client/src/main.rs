use cursive::Cursive;
use cursive::*;

use eleventh::screens::WelcomeScreen;
use eleventh::theme;

fn main() {
    let mut app = Cursive::default();
    
    WelcomeScreen(&mut app);

    app.set_theme(theme::theme());
    app.run();
}