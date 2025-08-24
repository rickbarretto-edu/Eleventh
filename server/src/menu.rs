use quickapi::response::Response;
use quickapi::server::Server;


pub fn route_menu(app: &mut Server) {

    app.route("GET", "/menu", |req, params| 
        Response::ok().plain("This is the menu route!")
    );

    app.route("POST", "/menu", |req, params| 
        Response::ok().plain(
            &format!("This is a POST request to /menu with body: {}", req.body)
        )
    );

}