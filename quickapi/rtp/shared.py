

import attrs


@attrs.frozen
class Version:
    number: str

    def __str__(self) -> str:
        return f"RTP/{self.number}"
