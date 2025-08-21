from quickapi import tcp
from quickapi.protocols.generic.body import Body
from quickapi.protocols.generic.parser.scan import EmptyMessage, parse_request_top, scan_body, scan_metadata, scan_transference
from quickapi.protocols.rtp.request import RTPRequest
from quickapi.protocols.rtp.shared import RTPVersion


async def parse_rtp_request(connection: tcp.Connection, buffer: str) -> tuple[RTPRequest | None, str]:
    head, tail = await scan_transference(connection, buffer)

    if head is None:
        return None, tail
    
    if not (lines := head.split("\r\n")):
        raise EmptyMessage
    
    method, path, version = parse_request_top(lines[0])
    metadata: dict[str, str] = scan_metadata(lines[:1])
    body_size: int = int(metadata["size"])
    body_type: str = metadata["type"]

    if body_size > 0:
        body, remainder = await scan_body(connection, tail, body_size)
    else:
        body, remainder = "", tail

    return RTPRequest(
        method=method,
        path=path,
        version=RTPVersion(version),
        body=Body(body, body_type)
    ), remainder