use cursive::view::*;
use cursive::views::Button;
use cursive::views::Dialog;
use cursive::views::EditView;
use cursive::views::LinearLayout;
use cursive::views::TextView;
use cursive::Cursive;
use cursive::*;

fn main() {
    let mut app = Cursive::default();

    WelcomeScreen(&mut app);
    app.run();
}

#[allow(non_snake_case)]
fn WelcomeScreen(app: &mut Cursive) {
    let content = &vec!["Eleventh", "Only 11 win!", "", "Press <Start> to begin."];
    let body = TextView::new(content.join("\n")).center();

    let view = Dialog::around(body)
        .title("Eleventh")
        .button("Start", |s| AccountMenu(s));

    app.add_layer(view);
}

#[allow(non_snake_case)]
fn AccountMenu(app: &mut Cursive) {
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

#[allow(non_snake_case)]
fn MainMenu(app: &mut Cursive) {
    app.pop_layer();

    let options = Dialog::text("Main Menu")
        .title("Main Menu")
        .button("Match", |s| MatchScreen(s))
        .button("Team", |s| TeamScreen(s))
        .button("Reward", |s| RewardScreen(s))
        .button("Quit", |s| s.quit());

    app.add_layer(options);
}

#[allow(non_snake_case)]
fn MatchScreen(app: &mut Cursive) {
    app.pop_layer();

    let options = Dialog::text("Match Screen")
        .title("Match")
        .button("Back to Main", |s| MainMenu(s));

    app.add_layer(options);
}

#[allow(non_snake_case)]
fn TeamScreen(app: &mut Cursive) {
    app.pop_layer();

    let options = Dialog::text("Team Screen")
        .title("Team")
        .button("Back to Main", |s| MainMenu(s));

    app.add_layer(options);
}

#[allow(non_snake_case)]
fn RewardScreen(s: &mut Cursive) {
    s.pop_layer();

    let options = Dialog::text("Reward Screen")
        .title("Reward")
        .button("Back to Main", |s| MainMenu(s));

    s.add_layer(options);
}
