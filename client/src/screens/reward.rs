use cursive::views::Dialog;
use cursive::Cursive;

use super::MainMenu;

#[allow(non_snake_case)]
pub fn RewardScreen(s: &mut Cursive, auth: String) {
    s.pop_layer();

    let options = Dialog::text("Reward Screen")
        .title("Reward")
        .button("Back to Main", move |s| MainMenu(s, auth.clone()));

    s.add_layer(options);
}
