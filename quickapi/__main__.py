import asyncio

from quickapi import QuickAPI
from quickapi.protocols.generic.body import Html, PlainText
from quickapi.protocols.generic.response import Status
from quickapi.protocols.http.request import HTTPRequest
from quickapi.protocols.http.response import HTTPResponse
from quickapi.router import Routes


async def _demo() -> None:

    app = Routes()

    @app.get("/")
    async def root(req: HTTPRequest) -> HTTPResponse:
        return HTTPResponse(Status.Ok, Html(
        f"""
        <h1>Hello, FastAPI-like Server</h1>
        <p>Method: {req.method}</p>
        <p>Target: {req.path}</p>
        """
        ))

    @app.post("/echo")
    async def echo(req: HTTPRequest) -> HTTPResponse:
        return HTTPResponse(Status.Ok, PlainText(f"You said: {req.body}"))

    await QuickAPI().serve(app)


if __name__ == "__main__":
    try:
        asyncio.run(_demo())
    except KeyboardInterrupt:
        pass