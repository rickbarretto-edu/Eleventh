use std::sync::Arc;
use std::sync::Mutex;

use cursive::Cursive;

use cursive::CursiveExt;
use eleventh::pages::Page;
use eleventh::pages::Welcome;


#[tokio::main]
pub async fn main() {

    let mut cursive = Arc::new(Mutex::new(Cursive::default()));

    let welcome = Arc::new(Welcome::new(cursive.clone()));
    // let account = Arc::new(Account::new());
    // let main = Arc::new(Main::new());

    // welcome.opens(account);
    // account.opens(main);
    // main.backs_to(welcome);

    welcome.render();
    cursive.lock().unwrap().run();

}