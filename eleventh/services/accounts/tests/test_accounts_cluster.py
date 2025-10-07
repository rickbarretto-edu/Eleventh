import asyncio
from typing import Iterable
from fastapi import FastAPI
from fastapi.testclient import TestClient

from eleventh.services.accounts import api
from eleventh.services.accounts import cluster

type Address = str

def create_addresses(n: int) -> list[Address]:
    return [f"http://localhost:{8000 + i}" for i in range(n)]

def create_peers(addresses: list[Address]) -> Iterable[tuple[FastAPI, Address]]:
    for address in addresses:
        app = FastAPI()
        app.include_router(api.route)
        app.include_router(cluster.route)
        app.add_middleware(cluster.ClusterMiddleware, address=address)
        yield app, address

def create_cluster(addresses: list[Address]) -> list[tuple[FastAPI, Address]]:
    peers: list[tuple[FastAPI, Address]] = list(create_peers(addresses))
    leader, _ = peers[0]
    others = peers[1:]

    with TestClient(leader) as client:
        for _, address in others:
            client.post("/accounts/cluster/attach/", json={
                "address": address,
            })

    return peers


def test_cluster_creation():
    """Scenario: Cluster Creation with Multiple Peers
    
    Given a list of 3 unique addresses,
    When peers attaches to each other,
    Then should have a cluster of 3 peers.
    """
    addresses = create_addresses(3)
    cluster = create_cluster(addresses)

    for app, address in cluster:
        with TestClient(app) as client:
            resp = client.get("/accounts/cluster/status/")
            data = resp.json()

            assert resp.status_code == 200
            assert data["address"] == address
            assert set(data["peers"]) == set(addresses)


def test_cluster_syncing():
    """Scenario: Cluster Syncing User Data
    
    Given a cluster of 3 peers,
    When a user signs up on one peer,
    Then the user data should be synced across all peers.
    """
    addresses = create_addresses(3)
    peers = create_cluster(addresses)

    # Sign up a user on the first peer
    first_app, first_address = peers[0]
    with TestClient(first_app) as client:
        resp = client.post("/accounts/signup/", json={
            "email": "user@example.com",
            "username": "user",
            "password": "password",
        })
        assert resp.status_code == 200

    asyncio.run(asyncio.sleep(1))
    
    for app, _ in peers:
        with TestClient(app) as client:
            resp = client.post("/accounts/login/", json={
                "email": "user@example.com",
                "password": "password",
            })

            assert resp.status_code == 200
            assert resp.json()["status"] == "valid"

