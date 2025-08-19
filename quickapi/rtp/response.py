from __future__ import annotations

import enum
from typing import Self

import attrs

from quickapi.rtp.body import Body

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
class Response:
    status: Status
    body: Body = Body("", "none")
    keep_alive: bool = False

    def keeping_alive(self) -> Self:
        return attrs.evolve(self, keep_alive=True)

    def __str__(self) -> str:
        return "\n".join([
            "{version} {code} {reason}",
            "size: {size}",
            "type: {type}",
            "connection: {connection}",
            "",
            "{body}"
        ]).format(
            version="RTP/1.0",
            code=self.status.code,
            reason=self.status.reason,
            size=len(self.body),
            type=self.body.type,
            connection="keep" if self.keep_alive else "close",
            body=self.body,
        )