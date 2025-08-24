

import textwrap
import json
from typing import Self
import attrs
import xml.dom.minidom

from quickapi.http.body import Body, MIMEType
from quickapi.http.response.status import Status
from quickapi.http.version import Version


@attrs.frozen
class HttpResponse:
    content: str = ""
    status: Status = Status.Ok
    mime: MIMEType = MIMEType("text", "plain")
    version: Version = Version("1.0")
    keep_alive: bool = False

    @property
    def body(self) -> Body:
        return Body(self.content, self.mime)

    @property
    def should_keep_alive(self) -> bool:
        return self.keep_alive

    def keeping_alive(self) -> Self:
        return attrs.evolve(self, keep_alive=True)

    def __str__(self) -> str:
        new_line = "\r\n"
        headers = [
            f"{self.version} {self.status.code} {self.status.reason}",
            f"Content-Length: {len(self.body)}",
        ]
        if len(self.body) > 0:
            headers.append(f"Content-Type: {self.mime}; charset=utf-8")
        headers.append(f"Connection: {'keep-alive' if self.keep_alive else 'close'}")
        return new_line.join(headers) + (new_line * 2) + str(self.body)


@attrs.frozen
class HtmlResponse(HttpResponse):
    def __attrs_post_init__(self) -> None:
        object.__setattr__(self, "mime", MIMEType("text", "html"))
        object.__setattr__(self, "content", textwrap.dedent(self.content).strip())


@attrs.frozen
class XmlResponse(HttpResponse):
    def __attrs_post_init__(self) -> None:
        object.__setattr__(self, "mime", MIMEType("application", "xml"))

        try:
            dom = xml.dom.minidom.parseString(self.content)
            pretty_xml = dom.toprettyxml(indent="  ")
            object.__setattr__(self, "content", pretty_xml.strip())
        except Exception:
            object.__setattr__(self, "content", self.content.strip())


@attrs.frozen
class JsonResponse(HttpResponse):
    content: dict = attrs.field(factory=dict)

    def __attrs_post_init__(self) -> None:
        object.__setattr__(self, "mime", MIMEType("application", "json"))
        object.__setattr__(self, "content", json.dumps(self.content, ensure_ascii=False))
