import attrs


@attrs.frozen
class Version:
    number: str = "1.1"

    def __str__(self) -> str:
        return f"HTTP/{self.number}"
