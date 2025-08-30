use cursive::views::Dialog;
use cursive::Cursive;
use std::sync::Arc;

type NextPage = Arc<dyn Fn(&mut Cursive) + Send + Sync>;

#[derive(Clone)]
pub struct Welcome {
    title: String,
    subtitle: String,
    instructions: String,
    next_page: NextPage,
}

impl Welcome {
    pub fn new(next: NextPage) -> Self {
        Self {
            title: "Eleventh".to_string(),
            subtitle: "Only 11 win!".to_string(),
            instructions: "Press <Start> to begin.".to_string(),
            next_page: next,
        }
    }

    pub fn message(&self) -> String {
        vec![
            self.title.as_str(),
            self.subtitle.as_str(),
            self.instructions.as_str(),
        ]
        .join("\n")
    }

    pub fn display(self, app: &mut Cursive) {
        let welcome = self.clone();
        app.add_layer(
            Dialog::text(self.message())
                .title("Welcome!")
                .button("Start", move |s| welcome.clone().show_next(s)),
        );
    }

    fn show_next(self, app: &mut Cursive) {
        app.pop_layer();
        (self.next_page)(app);
    }
}
