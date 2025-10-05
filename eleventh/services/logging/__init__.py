"""Logging service API.

This module defines the API routes for the logging service, allowing clients to interact with log data.
This service is intended for internal use, such as by admin or health check tools per peer.

This is not synced between peers; each peer maintains its own log store.

This also implements a publisher-subscriber model for log messages, allowing clients to subscribe
to real-time log updates via WebSocket.
"""

from eleventh.services.logging.api import route

__all__ = ["route"]