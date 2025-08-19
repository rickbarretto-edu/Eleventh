from __future__ import annotations

import enum

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