

import attrs


@attrs.frozen
class String:
    value: str

    def __str__(self) -> str:
        return self.value