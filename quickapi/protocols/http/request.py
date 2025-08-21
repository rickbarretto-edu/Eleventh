from __future__ import annotations

import attrs

from quickapi.protocols.generic import Body
from quickapi.protocols.generic.request import Request, Method, Path
from quickapi.protocols.http.version import HTTPVersion

@attrs.frozen
class HTTPRequest(Request):
    method: Method
    path: Path
    body: Body = Body("", "")
    keep_alive: bool = False

    @property
    def version(self) -> HTTPVersion:
        return HTTPVersion("1.0")

    def __str__(self) -> str:
        headers: list[str] = [
            "{method} {path} RTP/{version}",
            "Content-Length: {size}",
        ]

        if len(self.body) > 0:
            headers.append("Content-Type: {type}")

        headers.append("Connection: {connection}")
        headers.append("")
        headers.append("{body}")

        return "\n".join(headers).format(
            method=self.method,
            path=self.path,
            version=self.version,
            size=len(self.body),
            type=self.body.type,
            connection="keep-alive" if self.keep_alive else "close",
            body=self.body,
        )
