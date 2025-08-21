from typing import Self
import attrs

from quickapi.http.body import Body
from quickapi.http.request.method import Method
from quickapi.http.request.parse import from_connection
from quickapi.http.request.target import Target
from quickapi.http.version import Version


__all__ = [
    "Method",
    "from_connection",
    "Request",
    "Target",
]


@attrs.frozen
class Request:
    method: Method
    path: Target
    body: Body = Body.empty()
    keep_alive: bool = False

    @property
    def should_keep_alive(self) -> bool:
        return self.keep_alive

    @property
    def version(self) -> Version:
        return Version("1.0")

    def keeping_alive(self) -> Self:
        return attrs.evolve(self, keep_alive=True)

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
            type=self.body.mime,
            connection="keep-alive" if self.keep_alive else "close",
            body=self.body,
        )