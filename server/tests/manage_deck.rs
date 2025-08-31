use quickapi::server::Server;
use server::deck::route_decks;

#[tokio::test]
async fn user_can_claim_and_fire_cards() {
    let mut app = Server::new();
    route_decks(&mut app);

    // Initial deck should be empty
    let response = app.simulate("GET", "/user/123/deck/", "").await;
    assert_eq!(response.status, 200);
    let body: serde_json::Value = serde_json::from_str(&response.body).unwrap();
    assert!(body["players"].as_array().unwrap().is_empty());
    assert!(body["power_ups"].as_array().unwrap().is_empty());

    // Claim new deck
    let claim = app.simulate("GET", "/user/123/deck/claim", "").await;
    assert_eq!(claim.status, 200);
    let claim_body: serde_json::Value = serde_json::from_str(&claim.body).unwrap();
    assert_eq!(claim_body["message"], "You got new cards!");
    assert!(claim_body["players"].as_array().unwrap().len() > 0);

    // Claiming again within 24h fails
    let claim_again = app.simulate("GET", "/user/123/deck/claim", "").await;
    assert_eq!(claim_again.status, 400);
    let claim_again_body: serde_json::Value = serde_json::from_str(&claim_again.body).unwrap();
    assert_eq!(claim_again_body["message"], "Could not claim reward!");
    assert_eq!(claim_again_body["error"], "Reward already claimed in the last 24h");

    // Fire a card
    let fire = app.simulate("DELETE", "/user/123/deck/fire/0/", "").await;
    assert_eq!(fire.status, 200);
    let fire_body: serde_json::Value = serde_json::from_str(&fire.body).unwrap();
    assert_eq!(fire_body["message"], "Card removed from deck");

    // Check deck after firing
    let final_deck = app.simulate("GET", "/user/123/deck/", "").await;
    let final_body: serde_json::Value = serde_json::from_str(&final_deck.body).unwrap();
    assert_eq!(final_body["message"], "Your deck");
    assert_eq!(final_body["players"].as_array().unwrap().len(), claim_body["players"].as_array().unwrap().len() - 1);
}