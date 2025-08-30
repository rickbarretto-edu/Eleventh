use cursive::view::Nameable;
use cursive::views::{Dialog, EditView, LinearLayout, TextView};
use cursive::Cursive;

#[derive(Clone)]
pub struct Login {}

impl Login {
    pub fn new() -> Self {
        Self {}
    }

    pub fn display(self, app: &mut Cursive) {
        let form = LinearLayout::vertical()
            .child(TextView::new("Username:"))
            .child(EditView::new().with_name("username"))
            .child(TextView::new("Password:"))
            .child(EditView::new().secret().with_name("password"));

        let login_clone = self.clone();
        let create_clone = self.clone();

        app.add_layer(
            Dialog::around(form)
                .title("Account")
                .button("Login", move |app| login_clone.handle(app, "Login"))
                .button("Create", move |app| create_clone.handle(app, "Create"))
                .button("Quit", |app| app.quit()),
        );
    }

    fn handle(&self, app: &mut Cursive, action: &str) {
        let username = app
            .call_on_name("username", |view: &mut EditView| view.get_content())
            .unwrap();
        let password = app
            .call_on_name("password", |view: &mut EditView| view.get_content())
            .unwrap();

        app.add_layer(Dialog::info(format!(
            "{} account:\nUsername: {}\nPassword: {}",
            action, username, password
        )));
    }
}