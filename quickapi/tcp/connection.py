import asyncio
import contextlib
from functools import cached_property
import socket as native_socket
from typing import Self

import attrs

from .shared import Socket, EventLoop, ContextManager, Address

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
        with contextlib.suppress(OSError):
            self.socket.shutdown(native_socket.SHUT_RDWR)
            self.socket.close()
