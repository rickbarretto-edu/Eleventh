from typing import Self
import attrs

from quickapi.http.body import Body, MIMEType
from quickapi.http.response.status import Status
from quickapi.http.version import Version


@attrs.frozen
class Response:
    status: Status = Status.Ok
    body: Body = Body.empty()
    keep_alive: bool = False

    @classmethod
    def from_str(cls, content: str, status: Status = Status.Ok) -> Self:
        return cls(status=status, body=Body(content, MIMEType("text", "plain")))

    @property
    def should_keep_alive(self) -> bool:
        return self.keep_alive
    
    def keeping_alive(self) -> Self:
        return attrs.evolve(self, keep_alive=True)

    version: Version = attrs.field(default=Version("1.1"), init=False)

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
            type=self.body.mime,
            connection="keep-alive" if self.keep_alive else "close",
            body=self.body,
        )
