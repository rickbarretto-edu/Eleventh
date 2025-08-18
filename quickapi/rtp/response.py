from __future__ import annotations

import enum

import attrs

@attrs.frozen
class Response:
    status: Status
    body: Body

    def __str__(self) -> str:
        return "\n".join([
            "{version} {code} {reason}",
            "size: {size}",
            "type: {type}",
            "",
            "{body}"
        ]).format(
            version="RTP/1.0",
            code=self.status.code,
            reason=self.status.reason,
            size=len(self.body),
            type=self.body.type,
            body=self.body,
        )


class Status(enum.Enum, tuple):
    Ok       = (200, "Ok")
    NotFound = (400, "Not Found")

    @property
    def code(self) -> int:
        return self.value[0]
    
    @property
    def reason(self) -> str:
        return self.value[1]
    
    @property
    def description(self) -> str:
        return self.reason

    def __str__(self) -> str:
        return f"{self.code} {self.reason}"


@attrs.frozen
class Body:
    content: str
    type: str

    @property
    def bytes(self) -> int:
        return len(self.as_bytes())

    def as_bytes(self) -> bytes:
        return self.content.encode("utf-8", "replace")

    def __str__(self) -> str:
        return self.content

    def __len__(self) -> int:
        return self.bytes


class Html(Body):
    content: str

    @property
    def type(self) -> str:
        return "html"

class Json(Body):
    content: str

    @property
    def type(self) -> str:
        return "json"

class PlainText(Body):
    content: str

    @property
    def type(self) -> str:
        return "text"

class Xml(Body):
    content: str

    @property
    def type(self) -> str:
        return "xml"