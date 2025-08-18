from __future__ import annotations
import enum

import attrs


@attrs.frozen
class Request:
    method: Method
    path: Path
    body: Body

    def __str__(self) -> str:
        return "\n".join([
            f"{self.method} {self.path} RTP",
            f"size: {len(self.body)}",
            f"type: {self.body.type}"
            "",
            str(self.body)
        ])

@attrs.frozen
class Path:
    value: str

class Method(enum.StrEnum):
    Get = "GET"
    Post = "POST"

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
