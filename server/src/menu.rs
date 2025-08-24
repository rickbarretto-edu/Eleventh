use quickapi::response::Response;
use quickapi::server::Server;


pub fn route_menu(app: &mut Server) {

    app.get("/menu", |req, params| 
        Response::ok().plain("This is the menu route!")
    );

    app.post("/menu", |req, params| 
        Response::ok().plain(
            &format!("This is a POST request to /menu with body: {}", req.body)
        )
    );

}