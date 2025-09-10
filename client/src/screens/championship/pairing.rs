use cursive::Cursive;
use cursive::views::Dialog;
use std::time::{Duration, Instant};
use std::thread;

use super::NamePlayers;

fn fetch(start: Instant) -> bool {
    start.elapsed() >= Duration::from_millis(3500)
}

#[allow(non_snake_case)]
pub fn Pairing(app: &mut Cursive, auth: String) {
    let view = Dialog::new()
        .title("Pairing...")
        .button("Cancel", |app| {
            app.pop_layer();
        });

    app.add_layer(view);

    let sink = app.cb_sink().clone();
    let auth = auth.clone();
    let start = Instant::now();

    thread::spawn(move || {
        loop {
            thread::sleep(Duration::from_secs(1));
            if fetch(start) {
                let auth = auth.clone();
                sink.send(Box::new(move |app: &mut Cursive| {
                    NamePlayers(app, auth.clone());
                })).unwrap();
                break;
            }
        }
    });
}
