

import asyncio
from typing import Awaitable, Callable
import attrs

from quickapi import tcp
from quickapi.protocols.http.response import HTTPResponse
from quickapi.router import Routes
from quickapi.protocols.generic import Html, PlainText
from quickapi.protocols.generic.request import Request
from quickapi.protocols.generic.response import Response, Status
from quickapi.protocols.http import parser

async def _not_found(req: Request) -> HTTPResponse:
    return HTTPResponse(Status.NotFound)


@attrs.frozen
class QuickAPI:
    server: tcp.Server = tcp.Server()
    app: Callable[[Request], Awaitable[Response]] = _not_found

    async def serve(self, routes: Routes) -> None:
        await attrs.evolve(self, app=routes).forever()

    async def forever(self) -> None:
        async with self.server.handles(self._connection) as server:
            host, port = self.server.address
            print(f"Listening on rtp://{host}:{port}")
            await server.forever()

    async def _connection(self, connection: tcp.Connection) -> None:
        async with connection:
            buffer = ""
            while True:
                request, buffer = await parser.parse_http_request(connection, buffer)
                if request is None:
                    return

                try:
                    response = await self.app(request)
                except Exception:
                    response = HTTPResponse(Status.ServerError)

                if request.should_keep_alive:
                    await connection.send(str(response.keeping_alive()))
                else:
                    await connection.send(str(response))
                    return
