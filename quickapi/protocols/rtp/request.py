from __future__ import annotations

import attrs

from quickapi.protocols.generic import Body
from quickapi.protocols.generic.request import Request, Method, Path
from quickapi.protocols.rtp.shared import RTPVersion

@attrs.frozen
class RTPRequest(Request):
    method: Method
    path: Path
    body: Body = Body("", "")
    keep_alive: bool = False
    version: RTPVersion = RTPVersion("1.0")

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