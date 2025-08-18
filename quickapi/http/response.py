from __future__ import annotations

import enum

import attrs

@attrs.frozen
class Response:
    status: Status
    body: Body

    def __str__(self) -> str:
        return "\n".join([
            str(self.status),
            f"size: {len(self.body)}",
            "",
            "",
            f"{self.body}"
        ])


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
    pass

class Json(Body):
    pass

class PlainText(Body):
    pass

class Xml(Body):
    pass