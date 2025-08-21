from quickapi import tcp
from quickapi.http.body import Body, MIMEType
from quickapi.http import parse
from quickapi.http.parse import scan
from quickapi.http.request import Request
from quickapi.http.request.method import Method
from quickapi.http.request.target import Target
from quickapi.http.version import Version


__all__ = ["from_connection"]


class EmptyMessage(ValueError):
    pass


class MalformedMessage(ValueError):
    pass


def _request_top(line: str) -> tuple[Method, Target, Version]:
    try:
        method, path, version = line.split(" ", 2)
        return Method(method), Target(path), Version.from_str(version)
    except ValueError:
        raise MalformedMessage(f"Syntax error at: {line}") from ValueError


async def from_connection(connection: tcp.Connection, buffer: str) -> tuple[Request | None, str]:
    head, tail = await scan.frame(connection, buffer)

    if head is None:
        return None, tail

    if not (lines := head.split("\r\n")):
        raise EmptyMessage
    
    method, path, version = _request_top(lines[0])
    metadata: dict[str, str] = parse.metadata(lines[:1])
    body_size: int = int(metadata["Content-Length"])
    body_type: str = metadata.get("Content-Type", "")

    if version != Version("1.1"):
        supported_version = "QuickAPI supports HTTP/1.1 only"
        raise ValueError(supported_version)

    if body_size > 0:
        body, remainder = await scan.body(connection, tail, body_size)
    else:
        body, remainder = "", tail

    return Request(
        method=method,
        path=path,
        body=Body(body, MIMEType.from_str(body_type))
    ), remainder
    