import asyncio

from quickapi import QuickAPI
from quickapi.http.response import HtmlResponse, Response
from quickapi.http.request import Request
from quickapi.http.server import HTTPServer
from quickapi.router import Routes


async def _demo() -> None:

    app = Routes()

    @app.get("/")
    async def root(req: Request) -> Response:
        print(req)
        resp = HtmlResponse(
            f"""<!DOCTYPE html>
                <html>
                    <h1>Hello, from QuickAPI!</h1>
                    <p>Method: <b>{req.method}</b></p>
                    <p>Target: <b>{req.target}</b></p>
                </html>
            """
        )
        print(resp)
        return resp

    @app.post("/echo")
    async def echo(req: Request) -> Response:
        return Response(f"You said {req.body}")

    await QuickAPI().serve(app)


if __name__ == "__main__":
    try:
        asyncio.run(_demo())
    except KeyboardInterrupt:
        pass