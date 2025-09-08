use cursive::views::{Dialog, SelectView};
use cursive::Cursive;
use reqwest::blocking::Client;

use super::MainMenu;

pub fn MatchScreen(app: &mut Cursive, auth: String) {
    app.pop_layer();

    let options = Dialog::new()
        .button("Start Match", move |s| {
            let auth = auth.clone();
            let result = block_on_match_request(&auth, &format!("/match/{}/start/", auth));
            s.pop_layer();
            s.add_layer(
                Dialog::text(format!("Start result:\n{result}"))
                    .title("Match Result")
                    .button("Back", |_| {}),
            );
        });

    let dialog = Dialog::around(options)
        .title("Match Menu")
        .button("Back to Main", move |_| {});

    app.add_layer(dialog);
}

fn block_on_match_request(auth: &str, endpoint: &str) -> String {
    let client = Client::new();
    let url = format!("http://127.0.0.1:8080{}", endpoint);

    let res = client
        .post(&url)
        .header("Authorization", auth)
        .send();

    match res {
        Ok(resp) => match resp.text() {
            Ok(text) => text,
            Err(e) => format!("Failed to read response: {}", e),
        },
        Err(e) => format!("Request error: {}", e),
    }
}
