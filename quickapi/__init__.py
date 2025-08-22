from typing import Awaitable, Callable
import attrs

from quickapi import tcp
from quickapi.http.body import Body, MIMEType
from quickapi.http.request import Request
from quickapi.http.request import parse as request_parse
from quickapi.http.request.method import Method
from quickapi.http.request.target import Target
from quickapi.http.response import HtmlResponse, Response, Status
from quickapi.router import Routes

async def _not_found(req: Request) -> Response:
    return Response(status=Status.NotFound)

__all__ = [
    "QuickAPI",
    "Request",
    "Response",
    "HtmlResponse",
    "Routes",
    "Status",
]

@attrs.frozen
class QuickAPI:
    server: tcp.Server = tcp.Server()
    app: Callable[[Request], Awaitable[Response]] = _not_found

    async def serve(self, routes: Routes) -> None:
        await attrs.evolve(self, app=routes).forever()

    async def forever(self) -> None:
        async with self.server.handles(self._connection) as server:
            host, port = self.server.address
            print(f"Listening on http://{host}:{port}")
            await server.forever()

    async def _connection(self, connection: tcp.Connection) -> None:
        async with connection:
            buffer = ""
            while True:
                print(buffer)
                request, buffer = await request_parse.from_connection(connection, buffer)
                if request is None:
                    return

                try:
                    response = await self.app(request)
                except Exception:
                    response = Response(status=Status.ServerError)

                if request.should_keep_alive:
                    await connection.send(str(response.keeping_alive()))
                else:
                    await connection.send(str(response))
                    return
