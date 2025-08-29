use quickapi::{Server, Response};


pub fn route_menu(app: &mut Server) {

    app.get("/menu", |_req, _params| async move {
        Response::ok().plain("This is the menu route!")
    });

}