import pytest

from quickapi.http.response import Response, Status
from quickapi.http.request import Request, Method, Target
from quickapi.router import Endpoints, Routes


@pytest.mark.asyncio
async def test_manual_routing():
    endpoints = Endpoints()

    async def sample_action(req):
        return Response("ok")

    method = Method("GET")
    path = Target("/test")


    endpoints.add(method, path, sample_action)
    action = endpoints.of(method, path)
    response = await action(Request(method, path))

    assert isinstance(response, Response)
    assert response.status == Status.Ok
    assert response.body.content == "ok"


@pytest.mark.asyncio
async def test_at_routing():
    endpoints = Endpoints()
    routes = Routes(endpoints)

    @routes.at("/hello", "GET")
    async def hello_action(req):
        return Response("hello")

    request = Request(Method.get(), Target("/hello"))
    response = await routes(request)

    assert response.status == Status.Ok
    assert response.body.content == "hello"


@pytest.mark.asyncio
async def test_dynamic_routing():
    endpoints = Endpoints()
    routes = Routes(endpoints)

    @routes.post("/submit")
    async def submit_action(req):
        return Response("submitted", Status.Ok)

    request = Request(Method.post(), Target("/submit"))
    response = await routes(request)

    assert response.status == Status.Ok
    assert response.body.content == "submitted"


@pytest.mark.asyncio
async def test_not_found():
    endpoints = Endpoints()
    routes = Routes(endpoints)

    request = Request(Method.get(), Target("/missing"))
    response = await routes(request)

    assert response.status == Status.NotFound
    assert response.body.content == "404 Not Found"


@pytest.mark.asyncio
async def test_merged_routes():
    players = Routes()

    @players.get("/player/007")
    async def get_player(req):
        return Response("James Bond")

    missions = Routes()

    @missions.put("/mission/1")
    async def new_mission(req):
        return Response("Mission Created!")

    app = players | missions

    # Test player endpoint
    player_request = Request(Method("GET"), Target("/player/007"))
    player_response = await app(player_request)
    assert player_response.status == Status.Ok
    assert player_response.body.content == "James Bond"

    # Test mission endpoint
    mission_request = Request(Method("PUT"), Target("/mission/1"))
    mission_response = await app(mission_request)
    assert mission_response.status == Status.Ok
    assert mission_response.body.content == "Mission Created!"

    # Test Missing endpoint
    req_missing = Request(Method("GET"), Target("/missing"))
    resp_missing = await app(req_missing)
    assert resp_missing.status == Status.NotFound
    assert resp_missing.body.content == "404 Not Found"
