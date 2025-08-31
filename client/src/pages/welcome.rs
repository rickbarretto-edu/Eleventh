use std::sync::{Arc, Mutex};
use cursive::views::Dialog;
use cursive::Cursive;
use super::Page;

pub struct Welcome {
    ctx: Arc<Mutex<Cursive>>,
    next: Option<Arc<dyn Page + Send + Sync>>,
}

impl Welcome {
    pub fn new(ctx: Arc<Mutex<Cursive>>) -> Self {
        Self { ctx, next: None }
    }

    pub fn opens(&mut self, next: Arc<dyn Page + Send + Sync>) {
        self.next = Some(next);
    }

    fn message() -> String {
        vec![
            "Eleventh",
            "Only 11 win!",
            "Press <Start> to begin."
        ].join("\n")
    }
}

impl Page for Welcome {
    fn context(&self) -> Arc<Mutex<Cursive>> {
        self.ctx.clone()
    }

    fn render(&self) {
        let ctx = self.context();
        let mut context = ctx.lock().unwrap();

        let next_page = self.next.clone();

        let dialog = Dialog::text(Self::message())
            .title("Welcome!")
            .button("Start", move |_s| {
                if let Some(next) = &next_page {
                    next.render();
                }
            });

        context.pop_layer();
        context.add_layer(dialog);
    }
}
