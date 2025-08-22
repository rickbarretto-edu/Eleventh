
import asyncio
import contextlib
import socket

import attrs

__all__ = [
    "Address",
    "ContextManager",
    "EventLoop",
    "Socket",
]

Socket = socket.socket
ContextManager = contextlib.AbstractAsyncContextManager

type RunningLoop = asyncio.AbstractEventLoop
type EventLoop = asyncio.AbstractEventLoop


@attrs.frozen
class Address:
    host: str
    port: int

    def __str__(self) -> str:
        return f"{self.host}:{self.port}"