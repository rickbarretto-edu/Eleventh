"""Async TCP Server and Client implementation."""

import asyncio
import socket as socket_api
import contextlib as ctx
from functools import cached_property
from typing import Awaitable, Callable, Self

import attrs

__all__ = [
    "Client",
    "Server",
]


Socket = socket_api.socket
ContextManager = ctx.AbstractAsyncContextManager

type RunningLoop = asyncio.AbstractEventLoop
type EventLoop = asyncio.AbstractEventLoop


@attrs.frozen
class Address:
    host: str
    port: int

    def __str__(self) -> str:
        return f"{self.host}:{self.port}"


@attrs.frozen
class Connection(ContextManager):
    socket: Socket
    
    _loop: EventLoop = attrs.field(factory=asyncio.get_running_loop)

    @cached_property
    def address(self) -> Address:
        host, port = self.socket.getpeername()
        return Address(host, port)

    async def receive(self, n: int = 4096) -> str:
        data = await self._loop.sock_recv(self.socket, n)
        return data.decode() if data else ""

    async def send(self, data: str) -> None:
        await self._loop.sock_sendall(self.socket, data.encode())

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        with ctx.suppress(OSError):
            self.socket.shutdown(socket_api.SHUT_RDWR)
            self.socket.close()


@attrs.frozen
class Client(ContextManager):
    host: str
    port: int
    timeout: float | None = None

    _loop: EventLoop = attrs.field(factory=asyncio.get_event_loop)

    @classmethod
    def to(cls, host: str, at: int) -> Self:
        return cls(host=host, port=at)

    @classmethod
    def to_localhost(cls, at: int) -> Self:
        return cls.to("localhost", at)

    @cached_property
    def socket(self) -> Socket:
        socket = Socket(socket_api.AF_INET, socket_api.SOCK_STREAM)
        socket.setblocking(False)
        return socket

    async def __aenter__(self) -> Self:
        try:
            connect = self._loop.sock_connect(self.socket, (self.host, self.port))
            if self.timeout is not None:
                await asyncio.wait_for(connect, self.timeout)
            else:
                await connect
        except Exception:
            with ctx.suppress(OSError):
                self.socket.close()
            raise
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        with ctx.suppress(OSError):
            self.socket.shutdown(socket_api.SHUT_RDWR)
            self.socket.close()

    async def send(self, data: str) -> None:
        await self._loop.sock_sendall(self.socket, data.encode())

    async def receive(self, n: int = 4096) -> str:
        data = await self._loop.sock_recv(self.socket, n)
        return data.decode() if data else ""


type Handler = Callable[[Connection], Awaitable]

async def default_handler(connection: Connection) -> None:
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
    _handler: Handler = attrs.field(default=default_handler, alias="handles")

    _loop: EventLoop = attrs.field(factory=asyncio.get_event_loop)

    _client_tasks: set[asyncio.Task] = set()
    _accept_task: asyncio.Task | None = None

    @cached_property
    def socket(self) -> Socket:
        socket = Socket(socket_api.AF_INET, socket_api.SOCK_STREAM)
        socket.setsockopt(socket_api.SOL_SOCKET, socket_api.SO_REUSEADDR, 1)
        socket.setblocking(False)
        socket.bind((self.host, self.port))
        socket.listen(self.backlog)
        return socket

    @cached_property
    def address(self) -> tuple[str, int]:
        return self.socket.getsockname()

    async def forever(self) -> None:
        """Keep the server alive until externally cancelled."""
        with ctx.suppress(asyncio.CancelledError):
            while True:
                await asyncio.sleep(3600)

    async def __aenter__(self) -> Self:
        self._accept_task = self._loop.create_task(self._accept_loop())
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._accept_task:
            self._accept_task.cancel()
            with ctx.suppress(Exception):
                await self._accept_task

        for task in list(self._client_tasks):
            task.cancel()
            with ctx.suppress(Exception):
                await task

        with ctx.suppress(OSError):
            self.socket.shutdown(socket_api.SHUT_RDWR)
            self.socket.close()

    async def _accept_loop(self) -> None:
        with ctx.suppress(asyncio.CancelledError):
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
