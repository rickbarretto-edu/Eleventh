from typing import Awaitable, Callable, Optional, Self
import attrs
from quickapi import tcp
from quickapi.http.request import Request
from quickapi.http.request import parse as request_parse
from quickapi.http.response import Response
from quickapi.http.response.status import Status


async def not_found(req: Request) -> Response:
    return Response("404, Not Found!", Status.NotFound)

@attrs.define
class HTTPServer:
    host: str = "127.0.0.1"
    port: int = 8080
    backlog: int = 100
    app: Callable[[Request], Awaitable[Response]] = not_found

    _tcp: tcp.Server | None = None

    async def __aenter__(self) -> Self:
        self._tcp = tcp.Server(self.host, self.port, self.backlog).handles(self._handle_connection)
        await self._tcp.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        assert self._tcp is not None
        await self._tcp.__aexit__(exc_type, exc, tb)

    async def forever(self) -> None:
        assert self._tcp is not None
        await self._tcp.forever()

    async def _handle_connection(self, conn: tcp.Connection) -> None:
        async with conn:
            buffer = ""
            while True:
                request, buffer = await request_parse.from_connection(conn, buffer)

                if request is None:
                    break

                try:
                    response = await self.app(request)
                except Exception:
                    response = Response("500 Internal Server Error", Status.ServerError)

                if response.should_keep_alive:
                    await conn.send(str(attrs.evolve(response, keep_alive=response.should_keep_alive)))
                else:
                    break