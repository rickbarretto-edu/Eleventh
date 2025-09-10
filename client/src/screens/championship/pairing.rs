use cursive::Cursive;
use cursive::views::Dialog;
use std::time::{Duration, Instant};
use std::thread;

fn fetch(start: Instant) -> bool {
    start.elapsed() >= Duration::from_millis(3500)
}

#[allow(non_snake_case)]
pub fn Match(app: &mut Cursive, auth: String) {
    app.pop_layer();
    app.add_layer(Dialog::info(format!("Matched with auth: {}", auth)));
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
    let auth_clone = auth.clone();
    let start = Instant::now();

    thread::spawn(move || {
        loop {
            thread::sleep(Duration::from_secs(1));
            if fetch(start) {
                let auth_for_cb = auth_clone.clone();
                sink.send(Box::new(move |app: &mut Cursive| {
                    Match(app, auth_for_cb.clone());
                })).unwrap();
                break;
            }
        }
    });
}
