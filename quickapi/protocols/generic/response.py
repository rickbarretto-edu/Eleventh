from __future__ import annotations

import abc
import enum
from typing import Self

import attrs

from quickapi.protocols.generic.body import Body
from quickapi.protocols.generic.shared import Version

class Status(tuple, enum.Enum):
    Ok          = (200, "Ok")
    NotFound    = (400, "Not Found")
    ServerError = (500, "Internal Server Error")

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
class Response(abc.ABC):
    status: Status
    body: Body
    keep_alive: bool
    version: Version

    def keeping_alive(self) -> Self:
        return attrs.evolve(self, keep_alive=True)

    def __str__(self) -> str:
        raise NotImplemented