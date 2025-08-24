use quickapi::response::Response;
use quickapi::server::Server;


pub fn route_menu(app: &mut Server) {

    app.get("/menu", |_req, _params| 
        Response::ok().plain("This is the menu route!")
    );

}