import attrs


@attrs.frozen
class Body:
    content: str
    type: str

    @property
    def bytes(self) -> int:
        return len(self.as_bytes())

    def as_bytes(self) -> "bytes":
        return self.content.encode("utf-8", "replace")

    def __str__(self) -> str:
        return self.content

    def __len__(self) -> int:
        return self.bytes


class Html(Body):
    def __init__(self, content: str):
        super().__init__(content, "html")

class Json(Body):
    def __init__(self, content: str):
        super().__init__(content, "json")

class PlainText(Body):
    def __init__(self, content: str):
        super().__init__(content, "text")

@attrs.frozen
class Xml(Body):
    def __init__(self, content: str):
        super().__init__(content, "xml")