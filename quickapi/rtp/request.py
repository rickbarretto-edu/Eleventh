from __future__ import annotations
from typing import Final

import attrs

@attrs.frozen
class Path:
    value: str

    def __str__(self) -> str:
        return self.value


class _MethodMeta(type):
    def __getattr__(cls, name: str) -> "Method":
        return cls(name)


class Method(metaclass=_MethodMeta):

    def __init__(self, value: str) -> None:
        self.value: Final[str] = value.upper()

    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"Method({self.value!r})"

    def __eq__(self, other) -> bool:
        if isinstance(other, Method):
            return self.value == other.value
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.value)

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
    def __init__(self, content: str):
        super().__init__(content, "json")

class PlainText(Body):
    def __init__(self, content: str):
        super().__init__(content, "text")

class Xml(Body):
    def __init__(self, content: str):
        super().__init__(content, "xml")


@attrs.frozen
class Request:
    method: Method
    path: Path
    body: Body = Body("", "")

    def __str__(self) -> str:
        return "\n".join([
            "{method} {path} {version}",
            "size: {size}",
            "type: {type}"
            "",
            "{body}"
        ]).format(
            version="RTP/1.0",
            method=self.method,
            path=self.path,
            size=len(self.body),
            type=self.body.type,
            body=self.body,
        )