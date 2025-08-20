from __future__ import annotations
import abc
from typing import Final, Self

import attrs

from quickapi.protocols.generic.body import Body
from quickapi.protocols.generic.shared import Version

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
class Request(abc.ABC):
    method: Method
    path: Path
    body: Body
    keep_alive: bool
    version: Version

    def should_keep_alive(self) -> bool:
        return self.keep_alive
    
    def __str__(self) -> str:
        raise NotImplemented
