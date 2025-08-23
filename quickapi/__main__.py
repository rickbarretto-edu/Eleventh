import asyncio

from quickapi import QuickAPI
from quickapi.http.response import HtmlResponse, Response
from quickapi.http.request import Request
from quickapi.router import Routes


async def demo() -> None:

    app = Routes()

    @app.get("/")
    async def root(req: Request) -> Response:
        return HtmlResponse(
            f"""
            <!DOCTYPE html>
            <html>
                <h1>Hello, from QuickAPI!</h1>
                <p>Method: <b>{req.method}</b></p>
                <p>Target: <b>{req.target}</b></p>
            </html>
            """
        )

    @app.post("/echo")
    async def echo(req: Request) -> Response:
        return Response(f"You said {req.body}")

    await QuickAPI().serve(app)


def main():
    try:
        asyncio.run(demo())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()