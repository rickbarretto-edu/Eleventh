from typing import Self
import attrs


@attrs.frozen
class Version:
    number: str = "1.1"

    @classmethod
    def from_str(cls, content: str) -> Self:
        _, number = content.split("/", 1)
        return cls(number)

    def __str__(self) -> str:
        return f"HTTP/{self.number}"
