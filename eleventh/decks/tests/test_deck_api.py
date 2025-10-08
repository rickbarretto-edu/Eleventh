"""Tests for the Deck API endpoints."""

from uuid import uuid4, UUID

from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from eleventh.decks.web.api import route, get_decks
from eleventh.decks.repo import InMemoryDecks


@pytest.fixture
def app():
    """Create a FastAPI app with the deck routes."""
    app = FastAPI()
    app.include_router(route)
    return app


@pytest.fixture
def decks():
    """Create a fresh InMemoryDecks instance for each test."""
    return InMemoryDecks()


@pytest.fixture
def client(app: FastAPI, decks: InMemoryDecks):
    """Create a test client with dependency override."""
    app.dependency_overrides[get_decks] = lambda: decks
    return TestClient(app)


@pytest.fixture
def user_id():
    """Generate a test user ID."""
    return str(uuid4())


@pytest.fixture
def sample_cards():
    """Sample cards for testing."""
    return [
        {"name": "Cristiano Ronaldo", "position": "ATK", "power": 95},
        {"name": "Lionel Messi", "position": "ATK", "power": 93},
        {"name": "Luka Modric", "position": "MID", "power": 87},
        {"name": "Sergio Ramos", "position": "DEF", "power": 88},
        {"name": "Manuel Neuer", "position": "GK", "power": 90},
    ]


class TestGetUserDeck:
    """Tests for GET /api/deck/{user_id}"""

    def test_get_empty_deck(self, client: TestClient, user_id: str):
        """Test getting an empty deck for a new user."""
        response = client.get(f"/api/deck/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_deck_with_cards(self, client: TestClient, user_id: str, sample_cards: list):
        """Test getting a deck after adding cards."""
        # First add some cards
        client.post(f"/api/deck/add/{user_id}", json=sample_cards[:3])
        
        # Then retrieve the deck
        response = client.get(f"/api/deck/{user_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert all("id" in card for card in data)
        assert all("name" in card for card in data)
        assert all("position" in card for card in data)
        assert all("power" in card for card in data)

    def test_get_deck_different_users(self, client: TestClient, sample_cards: list):
        """Test that different users have separate decks."""
        user1_id = str(uuid4())
        user2_id = str(uuid4())
        
        # Add cards to user1
        client.post(f"/api/deck/add/{user1_id}", json=sample_cards[:2])
        
        # Add cards to user2
        client.post(f"/api/deck/add/{user2_id}", json=sample_cards[2:4])
        
        # Check user1's deck
        response1 = client.get(f"/api/deck/{user1_id}")
        assert response1.status_code == 200
        assert len(response1.json()) == 2
        
        # Check user2's deck
        response2 = client.get(f"/api/deck/{user2_id}")
        assert response2.status_code == 200
        assert len(response2.json()) == 2


class TestAddCards:
    """Tests for POST /api/deck/add/{user_id}"""

    def test_add_single_card(self, client: TestClient, user_id: str):
        """Test adding a single card to a deck."""
        card = {"name": "Neymar Jr", "position": "ATK", "power": 89}
        
        response = client.post(f"/api/deck/add/{user_id}", json=[card])
        
        assert response.status_code == 200
        
        # Verify card was added
        deck_response = client.get(f"/api/deck/{user_id}")
        cards = deck_response.json()
        assert len(cards) == 1
        assert cards[0]["name"] == "Neymar Jr"
        assert cards[0]["position"] == "ATK"
        assert cards[0]["power"] == 89

    def test_add_multiple_cards(self, client: TestClient, user_id: str, sample_cards: list):
        """Test adding multiple cards at once."""
        response = client.post(f"/api/deck/add/{user_id}", json=sample_cards)
        
        assert response.status_code == 200
        
        # Verify all cards were added
        deck_response = client.get(f"/api/deck/{user_id}")
        cards = deck_response.json()
        assert len(cards) == len(sample_cards)

    def test_add_cards_to_existing_deck(self, client: TestClient, user_id: str, sample_cards: list):
        """Test adding cards to a deck that already has cards."""
        # Add initial cards
        client.post(f"/api/deck/add/{user_id}", json=sample_cards[:2])
        
        # Add more cards
        client.post(f"/api/deck/add/{user_id}", json=sample_cards[2:4])
        
        # Verify total count
        deck_response = client.get(f"/api/deck/{user_id}")
        cards = deck_response.json()
        assert len(cards) == 4

    def test_add_card_all_positions(self, client: TestClient, user_id: str):
        """Test adding cards with all valid positions."""
        positions = ["ATK", "MID", "DEF", "GK"]
        
        for position in positions:
            card = {"name": f"Player {position}", "position": position, "power": 80}
            response = client.post(f"/api/deck/add/{user_id}", json=[card])
            assert response.status_code == 200
        
        # Verify all positions
        deck_response = client.get(f"/api/deck/{user_id}")
        cards = deck_response.json()
        card_positions = [card["position"] for card in cards]
        assert set(card_positions) == set(positions)

    def test_add_card_with_min_power(self, client: TestClient, user_id: str):
        """Test adding a card with minimum power."""
        card = {"name": "Rookie Player", "position": "MID", "power": 1}
        
        response = client.post(f"/api/deck/add/{user_id}", json=[card])
        
        assert response.status_code == 200

    def test_add_card_with_max_power(self, client: TestClient, user_id: str):
        """Test adding a card with maximum power."""
        card = {"name": "Legend Player", "position": "ATK", "power": 100}
        
        response = client.post(f"/api/deck/add/{user_id}", json=[card])
        
        assert response.status_code == 200

    def test_card_ids_are_unique(self, client: TestClient, user_id: str):
        """Test that each card gets a unique ID."""
        cards = [
            {"name": "Player A", "position": "ATK", "power": 85},
            {"name": "Player B", "position": "MID", "power": 85},
            {"name": "Player C", "position": "DEF", "power": 85},
        ]
        
        client.post(f"/api/deck/add/{user_id}", json=cards)
        
        deck_response = client.get(f"/api/deck/{user_id}")
        deck_cards = deck_response.json()
        
        card_ids = [card["id"] for card in deck_cards]
        assert len(card_ids) == len(set(card_ids)), "Card IDs should be unique"

    def test_add_invalid_position(self, client: TestClient, user_id: str):
        """Test that invalid positions are rejected."""
        card = {"name": "Invalid Player", "position": "INVALID", "power": 80}
        
        response = client.post(f"/api/deck/add/{user_id}", json=[card])
        
        assert response.status_code == 422  # Validation error


class TestSellCards:
    """Tests for POST /api/deck/{user_id}/sell"""

    def test_sell_existing_card(self, client: TestClient, user_id: str):
        """Test selling a card that exists in the deck."""
        # Add a card
        card = {"name": "Kylian Mbappe", "position": "ATK", "power": 91}
        client.post(f"/api/deck/add/{user_id}", json=[card])
        
        # Get the card ID
        deck_response = client.get(f"/api/deck/{user_id}")
        cards = deck_response.json()
        card_id = cards[0]["id"]
        
        # Sell the card
        response = client.post(
            f"/api/deck/{user_id}/sell",
            json={"card": card_id}
        )
        
        assert response.status_code == 200
        
        # Verify card was removed
        deck_response = client.get(f"/api/deck/{user_id}")
        remaining_cards = deck_response.json()
        assert len(remaining_cards) == 0

    def test_sell_card_from_multiple(self, client: TestClient, user_id: str, sample_cards: list):
        """Test selling one card from a deck with multiple cards."""
        # Add multiple cards
        client.post(f"/api/deck/add/{user_id}", json=sample_cards)
        
        # Get a card ID to sell
        deck_response = client.get(f"/api/deck/{user_id}")
        cards = deck_response.json()
        initial_count = len(cards)
        card_to_sell_id = cards[0]["id"]
        
        # Sell the card
        response = client.post(
            f"/api/deck/{user_id}/sell",
            json={"card": card_to_sell_id}
        )
        
        assert response.status_code == 200
        
        # Verify count decreased by 1
        deck_response = client.get(f"/api/deck/{user_id}")
        remaining_cards = deck_response.json()
        assert len(remaining_cards) == initial_count - 1
        
        # Verify the specific card was removed
        remaining_ids = [card["id"] for card in remaining_cards]
        assert card_to_sell_id not in remaining_ids

    def test_sell_nonexistent_card(self, client: TestClient, user_id: str):
        """Test selling a card that doesn't exist (should not raise error)."""
        fake_card_id = str(uuid4())
        
        response = client.post(
            f"/api/deck/{user_id}/sell",
            json={"card": fake_card_id}
        )
        
        # Should succeed even if card doesn't exist (idempotent)
        assert response.status_code == 200

    def test_sell_card_wrong_user(self, client: TestClient, sample_cards: list):
        """Test that selling affects only the specified user's deck."""
        user1_id = str(uuid4())
        user2_id = str(uuid4())
        
        # Add cards to both users
        client.post(f"/api/deck/add/{user1_id}", json=sample_cards[:2])
        client.post(f"/api/deck/add/{user2_id}", json=sample_cards[2:4])
        
        # Get card from user1
        deck1_response = client.get(f"/api/deck/{user1_id}")
        user1_cards = deck1_response.json()
        card_to_sell = user1_cards[0]["id"]
        
        # Sell card from user2's perspective (card doesn't exist there)
        client.post(f"/api/deck/{user2_id}/sell", json={"card": card_to_sell})
        
        # Verify user1 still has the card
        deck1_response = client.get(f"/api/deck/{user1_id}")
        user1_cards_after = deck1_response.json()
        assert len(user1_cards_after) == 2
        
        # Verify user2's deck unchanged
        deck2_response = client.get(f"/api/deck/{user2_id}")
        user2_cards = deck2_response.json()
        assert len(user2_cards) == 2


class TestIntegration:
    """Integration tests for complete workflows."""

    def test_full_deck_management_workflow(self, client: TestClient):
        """Test a complete workflow: add cards, view deck, sell cards."""
        user_id = str(uuid4())
        
        # Step 1: Verify empty deck
        response = client.get(f"/api/deck/{user_id}")
        assert len(response.json()) == 0
        
        # Step 2: Add initial cards
        initial_cards = [
            {"name": "Player 1", "position": "ATK", "power": 85},
            {"name": "Player 2", "position": "MID", "power": 80},
            {"name": "Player 3", "position": "DEF", "power": 78},
        ]
        client.post(f"/api/deck/add/{user_id}", json=initial_cards)
        
        # Step 3: Verify cards were added
        response = client.get(f"/api/deck/{user_id}")
        deck = response.json()
        assert len(deck) == 3
        
        # Step 4: Add more cards
        more_cards = [
            {"name": "Player 4", "position": "GK", "power": 82},
        ]
        client.post(f"/api/deck/add/{user_id}", json=more_cards)
        
        # Step 5: Verify total
        response = client.get(f"/api/deck/{user_id}")
        deck = response.json()
        assert len(deck) == 4
        
        # Step 6: Sell a card
        card_to_sell = deck[1]["id"]
        client.post(f"/api/deck/{user_id}/sell", json={"card": card_to_sell})
        
        # Step 7: Verify final state
        response = client.get(f"/api/deck/{user_id}")
        final_deck = response.json()
        assert len(final_deck) == 3
        assert card_to_sell not in [card["id"] for card in final_deck]

