pub mod login;
pub mod welcome;

use std::sync::Arc;
use std::sync::Mutex;

use cursive::Cursive;

pub trait Page {

    fn context(&self) -> Arc<Mutex<Cursive>>;
    fn render(&self);

} 

pub use welcome::Welcome;
// pub use login::Login;