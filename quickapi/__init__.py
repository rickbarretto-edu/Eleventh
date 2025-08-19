

from typing import Awaitable, Callable
import attrs

from quickapi import tcp
from quickapi.rtp.request import Request
from quickapi.rtp.response import Response, Status
from quickapi.rtp import parser

async def _not_found(req: Request) -> Response:
    return Response(Status.NotFound)


@attrs.frozen
class QuickAPI:
    server: tcp.Server
    app: Callable[[Request], Awaitable[Response]] = _not_found

    async def forever(self) -> None:
        async with self.server.handles(self._connection) as server:
            print(f"Listening on {self.server.address}")
            await server.forever()

    async def _connection(self, connection: tcp.Connection) -> None:
        async with connection:
            buffer = ""
            while True:
                request, buffer = await parser.parse_rtp_request(connection, buffer)
                if request is None:
                    return

                try:
                    response = await self.app(request)
                except Exception:
                    response = Response(Status.ServerError)  

                await connection.send(str(response.with_connection(
                    "close" if request.should_close else "keep-alive"
                )))
                if request.should_close:
                    return
