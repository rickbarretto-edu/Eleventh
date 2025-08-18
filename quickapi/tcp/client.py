import asyncio
import contextlib
from functools import cached_property
import socket as native_socket
from typing import Self


import attrs

from .shared import ContextManager, EventLoop, Socket


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
    
    def with_timeout(self, of: float) -> Self:
        return attrs.evolve(self, timeout=of)

    @cached_property
    def socket(self) -> Socket:
        socket = Socket(native_socket.AF_INET, native_socket.SOCK_STREAM)
        socket.setblocking(False)
        return socket

    async def __aenter__(self) -> Self:
        try:
            connect = self._loop.sock_connect(self.socket, (self.host, self.port))
            if self.timeout:
                await connect
            else:
                await asyncio.wait_for(connect, self.timeout)
        except Exception:
            with contextlib.suppress(OSError):
                self.socket.close()
            raise
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        with contextlib.suppress(OSError):
            self.socket.shutdown(native_socket.SHUT_RDWR)
            self.socket.close()

    async def send(self, data: str) -> None:
        await self._loop.sock_sendall(self.socket, data.encode())

    async def receive(self, n: int = 4096) -> str:
        data = await self._loop.sock_recv(self.socket, n)
        return data.decode() if data else ""
