use quickapi::{Server, Response};


pub fn route_menu(app: &mut Server) {

    app.get("/menu", |_req, _params| 
        Response::ok().plain("This is the menu route!")
    );

}