from typing import Self
import attrs


@attrs.frozen
class MIMEType:
    type: str
    subtype: str

    def __str__(self) -> str:
        return f"{self.type}/{self.subtype}"


@attrs.frozen
class Body:
    content: str
    mime: MIMEType | None

    @classmethod
    def empty(cls) -> Self:
        return cls("", None)

    @property
    def bytes(self) -> int:
        return len(self.as_bytes())

    def as_bytes(self) -> "bytes":
        return self.content.encode("utf-8", "replace")

    def __str__(self) -> str:
        return self.content

    def __len__(self) -> int:
        return self.bytes
