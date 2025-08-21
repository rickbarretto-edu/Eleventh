import abc
import attrs


@attrs.frozen
class MIMEType:
    type: str
    subtype: str

    def __str__(self) -> str:
        return f"{self.type}/{self.subtype}"


class Body(abc.ABC):
    content: str
    mime: MIMEType

    @property
    def bytes(self) -> int:
        return len(self.as_bytes())

    def as_bytes(self) -> "bytes":
        return self.content.encode("utf-8", "replace")

    def __str__(self) -> str:
        return self.content

    def __len__(self) -> int:
        return self.bytes
