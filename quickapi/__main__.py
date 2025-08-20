import asyncio

from quickapi import QuickAPI
from quickapi.router import Routes
from quickapi.rtp.body import Html, PlainText
from quickapi.rtp.request import Request
from quickapi.rtp.response import Response, Status


async def _demo() -> None:

    app = Routes()

    @app.get("/")
    async def root(req: Request) -> Response:
        return Response(Status.Ok, Html(
        f"""
        <h1>Hello, FastAPI-like Server</h1>
        <p>Method: {req.method}</p>
        <p>Target: {req.path}</p>
        """
        ))

    @app.post("/echo")
    async def echo(req: Request) -> Response:
        return Response(Status.Ok, PlainText(f"You said: {req.body}"))

    await QuickAPI().serve(app)


if __name__ == "__main__":
    try:
        asyncio.run(_demo())
    except KeyboardInterrupt:
        pass