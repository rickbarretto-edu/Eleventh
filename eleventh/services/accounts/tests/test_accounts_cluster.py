import time

import httpx

from eleventh.services.accounts import DistributedAccountsService


def accounts_service() -> DistributedAccountsService:
    return DistributedAccountsService([
        ("localhost", 8000),
        ("localhost", 8001),
        ("localhost", 8002),
        ("localhost", 8003),
    ])


def test_cluster_syncing():
    """Scenario: Signup and then Login

    Given a cluster of N accounts services
    When I sign up a user on the leader
    Then after a short delay I can login as that user on every peer
    """

    with accounts_service() as cluster:
        host, port = cluster.peers()[0]
        response = httpx.post(f"http://{host}:{port}/accounts/signup/", json={
            "email": "user@example.com",
            "username": "user",
            "password": "password",
        }, timeout=5.0)

        assert response.status_code == 200

        time.sleep(1)

        for host, port in cluster.peers():
            response = httpx.post(f"http://{host}:{port}/accounts/login/", json={
                "email": "user@example.com",
                "password": "password",
            }, timeout=5.0)

            assert response.status_code == 200
            assert response.json()["status"] == "valid"
