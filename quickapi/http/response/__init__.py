from typing import Self
import attrs

from quickapi.http.body import Body, MIMEType
from quickapi.http.response.status import Status
from quickapi.http.version import Version


@attrs.frozen
class Response:
    content: str = ""
    status: Status = Status.Ok
    mime: MIMEType = MIMEType("text", "plain")

    keep_alive: bool = attrs.field(default=False, init=False)
    version: Version = attrs.field(default=Version("1.1"), init=False)

    @property
    def body(self) -> Body:
        return Body(self.content, self.mime)

    @property
    def should_keep_alive(self) -> bool:
        return self.keep_alive
    
    def keeping_alive(self) -> Self:
        return attrs.evolve(self, keep_alive=True)

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


@attrs.frozen
class HtmlResponse(Response):
    def __init__(self, content: str, status: Status = Status.Ok) -> None:
        super().__init__(
            content=content, 
            status=status, 
            mime=MIMEType("text", "html")
        )
