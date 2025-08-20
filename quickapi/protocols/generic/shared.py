import abc
import attrs


@attrs.frozen
class Version(abc.ABC):
    number: str

    def __str__(self) -> str:
        raise NotImplemented
