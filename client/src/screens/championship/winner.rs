use cursive::Cursive;
use cursive::views::{Dialog, TextView};
use std::time::{Duration};
use std::thread;

use crate::services;

#[allow(non_snake_case)]
pub fn Waiting(app: &mut Cursive, auth: String) {
    app.pop_layer();

    let view = Dialog::new()
        .title("Waiting for your opponnent...")
        .button("Close", |app| {app.pop_layer();});

    app.add_layer(view);

    let sink = app.cb_sink().clone();
    let auth = auth.clone();

    thread::spawn(move || {
        loop {
            thread::sleep(Duration::from_secs(1));
            if let Ok(state) = services::championship::status(&auth) {
                if let Some(winner) = state.winner {
                    let score = state.score.expect("Have Score");
                    let have_won = &winner == &auth;

                    let message = if have_won {
                        format!("You have won: {}x{}", score.0, score.1)
                    } else {
                        format!("You have lose: {}x{}", score.0, score.1)
                    };

                    sink.send(Box::new(move |app: &mut Cursive| {
                        Winner(app, message);
                    })).unwrap();
                    break;
                }
            }
        }
    });
}

#[allow(non_snake_case)]
fn Winner(app: &mut Cursive, message: String) {
    app.pop_layer();

    let view = Dialog::around(TextView::new(message))
        .title("Winner")
        .button("Close", |app| {app.pop_layer();});

    app.add_layer(view);
}
