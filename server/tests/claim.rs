
use quickapi::server::Server;
use server::deck::route_decks;

#[tokio::test]
async fn claims_a_new_deck_successfully() {
    let mut app = Server::new();
    route_decks(&mut app);

    let response = app.simulate("GET", "/user/123/deck/claim/", "").await;
    assert_eq!(response.status, 200);

    let body: serde_json::Value = serde_json::from_str(&response.body).unwrap();
    assert_eq!(body["message"], "You got new cards!");
    assert!(body["players"].is_array());
    assert!(body["power_ups"].is_array());
}

#[tokio::test]
async fn prevents_claiming_twice_in_24h() {
    let mut app = Server::new();
    route_decks(&mut app);

    // first claim
    let _ = app.simulate("GET", "/user/123/deck/claim/", "").await;

    // second claim
    let second = app.simulate("GET", "/user/123/deck/claim", "").await;
    assert_eq!(second.status, 400);

    let body: serde_json::Value = serde_json::from_str(&second.body).unwrap();
    assert_eq!(body["message"], "Could not claim reward!");
    assert_eq!(body["error"], "Reward already claimed in the last 24h");
}
