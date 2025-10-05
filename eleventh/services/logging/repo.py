

import contextlib
from typing import Protocol
import asyncio

import attrs


class Logs(Protocol):
    """Protocol for logging services."""

    async def all(self) -> list[str]:
        """Return all log messages."""
        ...

    async def log(self, message: str) -> None:
        """Log a message."""
        ...

    async def subscribe(self) -> "asyncio.Queue[str]":
        """Subscribe to future log messages."""
        ...

    async def unsubscribe(self, queue: "asyncio.Queue[str]") -> None:
        """Unsubscribe a previously returned queue."""
        ...


@attrs.frozen(slots=True)
class InMemoryLogs:
    """In-memory log store with simple subscriber support.

    Subscribers receive each new log entry via an asyncio.Queue. This
    enables streaming new logs to clients (SSE/WebSocket) without polling.
    """

    _logs: list[str] = attrs.field(factory=list)
    _subscribers: list[asyncio.Queue] = attrs.field(factory=list)

    async def all(self) -> list[str]:
        return [*self._logs]

    async def log(self, message: str) -> None:
        self._logs.append(message)
        self._notify_subscribers(message)

    def _notify_subscribers(self, message):
        for q in list(self._subscribers):
            with contextlib.suppress(Exception):
                q.put_nowait(message)

    async def subscribe(self) -> asyncio.Queue:
        queue = asyncio.Queue()
        self._subscribers.append(queue)
        return queue

    async def unsubscribe(self, queue: asyncio.Queue) -> None:
        with contextlib.suppress(ValueError):
            self._subscribers.remove(queue)
