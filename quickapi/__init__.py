

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
                    response = self.app(request)
                except Exception:
                    response = Response(Status.500)  

                to_send = response.alived if request.keep else response
                await connection.send(str(to_send))

                if response.should_keep:
                    await connection.send(str(response.alived))
                else:
                    await connection.send(str(response))
                    return


