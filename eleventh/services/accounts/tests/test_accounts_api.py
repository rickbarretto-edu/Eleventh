from fastapi import FastAPI
from fastapi.testclient import TestClient

from eleventh.services.accounts import api


def create_client() -> TestClient:
    """Create a TestClient for the API."""
    app = FastAPI()
    app.include_router(api.route)
    return TestClient(app)


def test_signup_success():
    """Scenario: Successful Signup Attempt

    When a user attempts to sign up with unique email and username,
    Then the response indicates success.
    """

    with create_client() as client:
        resp = client.post("/accounts/signup/", json={
            "email": "alice@example.com",
            "username": "alice",
            "password": "s3cr3t",
        })
        assert resp.status_code == 200
        assert resp.json() == {"status": "success"}


def test_signup_email_taken():
    """Scenario: Signup Attempt with Taken Email

    Given a user with 'alice@example.com' email,
    When another user attempts to sign up with the same email,
    Then the response indicates the email is taken.
    """

    with create_client() as client:
        resp1 = client.post("/accounts/signup/", json={
            "email": "alice@example.com",
            "username": "alice",
            "password": "s3cr3t",
        })
        assert resp1.status_code == 200

        resp2 = client.post("/accounts/signup/", json={
            "email": "alice@example.com",
            "username": "alice2",
            "password": "x",
        })
        assert resp2.status_code == 200
        assert resp2.json() == {"status": "email_taken"}


def test_signup_username_taken():
    """Scenario: Signup Attempt with Taken Username

    Given a user with 's3cr3t' password
        And 'alice@example.com' email,
    When another user attempts to sign up with the same username,
    Then the response indicates the username is taken.
    """

    with create_client() as client:
        resp1 = client.post("/accounts/signup/", json={
            "email": "alice@example.com",
            "username": "alice",
            "password": "s3cr3t",
        })
        assert resp1.status_code == 200

        resp2 = client.post("/accounts/signup/", json={
            "email": "bob@example.com",
            "username": "alice",
            "password": "y",
        })
        assert resp2.status_code == 200
        assert resp2.json() == {"status": "username_taken"}


def test_valid_login():
    """Scenario: Login Attempt for Valid Login

    Given a user with 's3cr3t' password
        And 'alice@example.com' email,
    When user attempts to log in with right password,
    Then the response indicates valid credentials,
        And returns its user's ID.
    """

    with create_client() as client:
        client.post("/accounts/signup/", json={
            "email": "alice@example.com",
            "username": "alice",
            "password": "s3cr3t",
        })

        login = client.post("/accounts/login/", json={
            "email": "alice@example.com",
            "password": "s3cr3t",
        })
        assert login.status_code == 200
        data = login.json()
        assert data.get("status") == "valid"
        assert "uuid" in data


def test_mismatched_password():
    """Scenario: Login Attempt for Mismatched Password

    Given a user with 's3cr3t' password
        And 'alice@example.com' email,
    When user attempts to log in with 'wrong' password,
    Then the response indicates invalid credentials.
    """

    with create_client() as client:
        client.post("/accounts/signup/", json={
            "email": "alice@example.com",
            "username": "alice",
            "password": "s3cr3t",
        })

        bad = client.post("/accounts/login/", json={
            "email": "alice@example.com",
            "password": "wrong",
        })
        assert bad.status_code == 200
        assert bad.json() == {"status": "invalid-credentials"}
