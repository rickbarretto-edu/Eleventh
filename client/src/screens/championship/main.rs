use cursive::views::{Dialog, SelectView};
use cursive::Cursive;
use reqwest::blocking::Client;

use crate::screens::MainMenu;
use crate::screens::NamePlayers;


#[allow(non_snake_case)]
pub fn ChampionshipMenu(app: &mut Cursive, auth: String) {
    let options = vec![
        ("Go".to_string(), "Go".to_string()),
        ("Back".to_string(), "Back".to_string()),
    ];

    let menu = SelectView::<String>::new()
        .autojump()
        .with_all(options)
        .on_submit(move |app, choice: &String| {
            let auth = auth.clone();
            match choice.as_str() {
                "Go" => on_go(app, &auth),
                "Back" => on_back(app, auth),
                _ => {}
            }
        });

    let main_dialog = Dialog::around(menu)
        .title("Championship")
        .button("Quit", |app| app.quit());

    app.add_layer(main_dialog);
}

/// Return to main menu when the user clicks in 'Back'
fn on_back(app: &mut Cursive, auth_clone: String) {
    app.pop_layer();
    MainMenu(app, auth_clone.clone());
}

/// Open next page or display error when the user clicks in 'Go'
fn on_go(app: &mut Cursive, auth: &String) {
    match join(auth) {
        Ok(_) => NamePlayers(app, auth.clone()),
        Err(err) => display_error(app, err)
    };
}

/// Display request error to end-user
fn display_error(app: &mut Cursive, err: String) {
    let error = Dialog::info(err)
        .title("Error");
    app.add_layer(error);
}

/// Join a player to a match
fn join(auth: &String) -> Result<String, String> {
    let client = Client::new();
    let url = format!("http://127.0.0.1:8080/match/{}/start/", auth);

    let response = client
        .post(&url)
        .header("Authorization", auth)
        .send();

    match response {
        Ok(resp) => match resp.text() {
            Ok(text) => Ok(text.into()),
            Err(e) => Err(format!("Failed to read response: {}", e)),
        },
        Err(e) => Err(format!("Request error: {}", e)),
    }
} 