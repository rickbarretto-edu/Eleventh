from __future__ import annotations
from typing import Final, Self

import attrs

from quickapi.rtp.body import Body
from quickapi.rtp.shared import Version

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
class Request:
    method: Method
    path: Path
    body: Body = Body("", "")
    keep_alive: bool = False
    version: Version = Version("1.0")

    def should_keep_alive(self) -> bool:
        return self.keep_alive

    def __str__(self) -> str:
        return "\n".join([
            "{method} {path} {version}",
            "size: {size}",
            "type: {type}",
            "connection: {connection}",
            "",
            "{body}"
        ]).format(
            version=self.version,
            method=self.method,
            path=self.path,
            size=len(self.body),
            type=self.body.type,
            connection="keep" if self.keep_alive else "close",
            body=self.body,
        )