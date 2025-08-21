from quickapi import tcp
from quickapi.protocols.generic.body import Body
from quickapi.protocols.generic.parser.scan import EmptyMessage, parse_request_top, scan_body, scan_metadata, scan_transference
from quickapi.protocols.http.request import HTTPRequest
from quickapi.protocols.http.version import HTTPVersion


async def parse_http_request(connection: tcp.Connection, buffer: str) -> tuple[HTTPRequest | None, str]:
    head, tail = await scan_transference(connection, buffer)

    if head is None:
        return None, tail
    
    if not (lines := head.split("\r\n")):
        raise EmptyMessage
    
    method, path, version = parse_request_top(lines[0])
    metadata: dict[str, str] = scan_metadata(lines[:1])
    body_size: int = int(metadata["Content-Length"])
    body_type: str = metadata.get("Content-Type", "")

    if body_size > 0:
        body, remainder = await scan_body(connection, tail, body_size)
    else:
        body, remainder = "", tail

    return HTTPRequest(
        method=method,
        path=path,
        version=HTTPVersion(version),
        body=Body(body, body_type)
    ), remainder
    
