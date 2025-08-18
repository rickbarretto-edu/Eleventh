import pytest

from quickapi.rtp.request import Request, Method, Path
from quickapi.rtp.response import Response, Status, PlainText
from quickapi.rtp.router import Endpoints, Routes


@pytest.mark.asyncio
async def test_manual_routing():
    endpoints = Endpoints()

    async def sample_action(req):
        return Response(Status.Ok, PlainText("ok"))

    method = Method("GET")
    path = Path("/test")


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
        return Response(Status.Ok, PlainText("hello"))

    request = Request(Method.GET, Path("/hello"))
    response = await routes(request)

    assert response.status == Status.Ok
    assert response.body.content == "hello"


@pytest.mark.asyncio
async def test_dynamic_routing():
    endpoints = Endpoints()
    routes = Routes(endpoints)

    @routes.post("/submit")
    async def submit_action(req):
        return Response(Status.Ok, body=PlainText("submitted"))

    request = Request(Method.Post, Path("/submit"))
    response = await routes(request)

    assert response.status == Status.Ok
    assert response.body.content == "submitted"


@pytest.mark.asyncio
async def test_not_found():
    endpoints = Endpoints()
    routes = Routes(endpoints)

    request = Request(Method.Get, Path("/missing"))
    response = await routes(request)

    assert response.status == Status.NotFound
    assert response.body.content == "404 Not Found"
