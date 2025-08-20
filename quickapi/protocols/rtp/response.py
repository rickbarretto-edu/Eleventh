from __future__ import annotations

import attrs

from quickapi.protocols.generic import Response, Body
from quickapi.protocols.generic.response import Status
from quickapi.protocols.rtp.shared import RTPVersion


@attrs.frozen
class RTPResponse(Response):
    status: Status
    body: Body = Body("", "none")
    keep_alive: bool = False
    version: RTPVersion = RTPVersion("1.0")

    def __str__(self) -> str:
        return "\n".join([
            "{version} {code} {reason}",
            "size: {size}",
            "type: {type}",
            "connection: {connection}",
            "",
            "{body}"
        ]).format(
            version=self.version,
            code=self.status.code,
            reason=self.status.reason,
            size=len(self.body),
            type=self.body.type,
            connection="keep" if self.keep_alive else "close",
            body=self.body,
        )