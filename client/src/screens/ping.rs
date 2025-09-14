use cursive::views::Dialog;
use cursive::Cursive;

#[allow(non_snake_case)]
pub fn Ping(app: &mut Cursive) {
    let view = Dialog::info("Ping feature is under construction.");
    app.add_layer(view);
}
