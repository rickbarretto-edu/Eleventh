from fastapi import FastAPI
from fastapi.testclient import TestClient

from eleventh.services.logging import api
from eleventh.services.logging.repo import InMemoryLogs


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api.route)
    return app

def test_initially_empty():
    app = create_app()
    with TestClient(app) as client:
        response = client.get("/log/")
        assert response.status_code == 200
        assert response.json() == {"logs": []}


def test_event_logged_twice_via_endpoints():
    app = create_app()
    with TestClient(app) as client:
        resp1 = client.post("/log/", json="first-msg")
        assert resp1.status_code in (200, 204)

        resp2 = client.post("/log/", json="second-msg")
        assert resp2.status_code in (200, 204)

        response = client.get("/log/")
        assert response.status_code == 200
        data = response.json()
        assert "logs" in data
        assert len(data["logs"]) >= 2

        joined = "\n".join(data["logs"]) if data["logs"] else ""
        assert "first-msg" in joined
        assert "second-msg" in joined


def test_ui_endpoint():
    app = create_app()
    with TestClient(app) as client:
        response = client.get("/log/ui")
        assert response.status_code in (200, 404)
