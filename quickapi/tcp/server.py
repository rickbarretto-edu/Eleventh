import asyncio
import contextlib
from functools import cached_property
import socket as native_socket
from typing import Awaitable, Callable, Self

import attrs

from quickapi.tcp.connection import Connection
from .shared import ContextManager, EventLoop, Socket


type Action = Callable[[Connection], Awaitable]

async def _echo(connection: Connection) -> None:
    async with connection:
        while True:
            if not (data := await connection.receive()):
                break
            await connection.send(data)


@attrs.define
class Server(ContextManager):
    host: str = "127.0.0.1"
    port: int = 0
    backlog: int = 100
    _handler: Action = attrs.field(default=_echo, alias="handles")

    _loop: EventLoop = attrs.field(factory=asyncio.get_event_loop)

    _client_tasks: set[asyncio.Task] = set()
    _accept_task: asyncio.Task | None = None

    @classmethod
    def at(cls, host: str, port: int) -> Self:
        return cls(host=host, port=port)

    @classmethod
    def local_at(cls, port: int) -> Self:
        return cls.at("localhost", port)
    
    def handles(self, action: Action) -> Self:
        return attrs.evolve(self, handles=action)

    @cached_property
    def socket(self) -> Socket:
        socket = Socket(native_socket.AF_INET, native_socket.SOCK_STREAM)
        socket.setsockopt(native_socket.SOL_SOCKET, native_socket.SO_REUSEADDR, 1)
        socket.setblocking(False)
        socket.bind((self.host, self.port))
        socket.listen(self.backlog)
        return socket

    @cached_property
    def address(self) -> tuple[str, int]:
        return self.socket.getsockname()

    async def forever(self) -> None:
        """Keep the server alive until externally cancelled."""
        with contextlib.suppress(asyncio.CancelledError):
            while True:
                await asyncio.sleep(3600)

    async def __aenter__(self) -> Self:
        self._accept_task = self._loop.create_task(self._accept_loop())
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._accept_task:
            self._accept_task.cancel()
            with contextlib.suppress(Exception):
                await self._accept_task

        for task in list(self._client_tasks):
            task.cancel()
            with contextlib.suppress(Exception):
                await task

        with contextlib.suppress(OSError):
            self.socket.shutdown(native_socket.SHUT_RDWR)
            self.socket.close()

    async def _accept_loop(self) -> None:
        with contextlib.suppress(asyncio.CancelledError):
            while True:
                client_sock, _ = await self._loop.sock_accept(self.socket)
                client_sock.setblocking(False)
                conn = Connection(client_sock, self._loop)
                task = self._loop.create_task(self._run_handler(conn))
                task.add_done_callback(self._client_tasks.discard)
                self._client_tasks.add(task)

    async def _run_handler(self, conn: Connection) -> None:
        try:
            await self._handler(conn)
        finally:
            await conn.__aexit__(None, None, None)