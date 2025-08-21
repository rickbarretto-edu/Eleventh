from __future__ import annotations

import attrs

from quickapi.protocols.generic import Response, Body
from quickapi.protocols.generic.response import Status
from quickapi.protocols.http.version import HTTPVersion


@attrs.frozen
class HTTPResponse(Response):
    status: Status
    body: Body = Body("", "")
    keep_alive: bool = False
    version = HTTPVersion("1.1")

    def __str__(self) -> str:
        headers: list[str] = [
            "{version} {code} {reason}",
            "Content-Length: {size}",
        ]

        if len(self.body) > 0:
            headers.append("Content-Type: {type}")

        headers.append("Connection: {connection}")
        headers.append("")
        headers.append("{body}")

        return "\n".join(headers).format(
            version=self.version,
            code=self.status.code,
            reason=self.status.reason,
            size=len(self.body),
            type=self.body.type,
            connection="keep-alive" if self.keep_alive else "close",
            body=self.body,
        )