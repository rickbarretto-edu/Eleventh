import asyncio

from quickapi import QuickAPI
from quickapi.http.response import HtmlResponse, Response, Status
from quickapi.http.request import Request
from quickapi.router import Routes


async def _demo() -> None:

    app = Routes()

    @app.get("/")
    async def root(req: Request) -> Response:
        return HtmlResponse(
            f"""
            <h1>Hello, FastAPI-like Server</h1>
            <p>Method: {req.method}</p>
            <p>Target: {req.path}</p>
            """
        )

    @app.post("/echo")
    async def echo(req: Request) -> Response:
        return Response(f"You said {req.body}")

    await QuickAPI().serve(app)


if __name__ == "__main__":
    try:
        asyncio.run(_demo())
    except KeyboardInterrupt:
        pass