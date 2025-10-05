

from typing import Protocol

import attrs


class Logs(Protocol):
    """Protocol for logging services."""

    async def all(self) -> list[str]:
        """Return all log messages."""
        ...

    async def log(self, message: str) -> None:
        """Log a message."""
        ...


@attrs.frozen(slots=True)
class InMemoryLogs:
    """In-memory log store with simple subscriber support.

    Subscribers receive each new log entry via an asyncio.Queue. This
    enables streaming new logs to clients (SSE/WebSocket) without polling.
    """

    _logs: list[str] = attrs.field(factory=list)

    async def all(self) -> list[str]:
        return [*self._logs]

    async def log(self, message: str) -> None:
        self._logs.append(message)
