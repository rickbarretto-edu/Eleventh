from quickapi import tcp
from quickapi.http.body import Body, MIMEType
from quickapi.http.parser.scan import EmptyMessage, parse_request_top, scan_body, scan_metadata, scan_transference
from quickapi.http.request import Request
from quickapi.http.version import Version


__all__ = ["from_connection"]


async def from_connection(connection: tcp.Connection, buffer: str) -> tuple[Request | None, str]:
    head, tail = await scan_transference(connection, buffer)

    if head is None:
        return None, tail

    if not (lines := head.split("\r\n")):
        raise EmptyMessage
    
    method, path, version = parse_request_top(lines[0])
    metadata: dict[str, str] = scan_metadata(lines[:1])
    body_size: int = int(metadata["Content-Length"])
    body_type: str = metadata.get("Content-Type", "")

    if version != Version("1.1"):
        supported_version = "QuickAPI supports HTTP/1.1 only"
        raise ValueError(supported_version)

    if body_size > 0:
        body, remainder = await scan_body(connection, tail, body_size)
    else:
        body, remainder = "", tail

    return Request(
        method=method,
        path=path,
        body=Body(body, MIMEType.from_str(body_type))
    ), remainder
    