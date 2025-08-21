

from quickapi import tcp
from quickapi.protocols.generic.body import Body
from quickapi.protocols.generic.request import Method, Path, Request
from quickapi.protocols.rtp.request import RTPRequest


class EmptyMessage(ValueError):
    pass

class MalformedMessage(ValueError):
    pass


async def scan_transference(connection: tcp.Connection, current_buffer: str):
    empty_line = "\r\n\r\n"
    buffer = list(current_buffer)

    while empty_line not in buffer:
        if (chunk := await connection.receive()):
            buffer += chunk
        else:
            return None, "".join(buffer)

    head, tail = "".join(buffer).split(empty_line, 1)
    return head, tail


def scan_metadata(lines: list[str]) -> dict[str, str]:
    separator = ":"

    def pair(line: str) -> tuple[str, str]:
        key, val = line.strip().split(separator, 1)
        return key.strip(), val.strip()

    def key(line: str) -> str:
        key, _ = pair(line)
        return key.lower()
    
    def value(line: str) -> str:
        _, val = pair(line)
        return val

    return {
        key(line): value(line)
        for line in lines
        if ":" in line
    }

def to_str_safe(content: bytes) -> str:
    return content.decode("replace")

def split_scannnig(content: bytes, size: int): 
    return (
        to_str_safe(content[:size]), 
        to_str_safe(content[size:])
    )

async def scan_body(connection: tcp.Connection, prev_buffer: str, size: int) -> tuple[str, str]:
    buffer: bytes = prev_buffer.encode()
    if len(buffer) >= size:
        return split_scannnig(buffer, size)
    
    return await scan_large_body(connection, buffer, size)

async def scan_large_body(connection: tcp.Connection, buffer: bytes, size: int) -> tuple[str, str]:
    chunks: list[bytes] = [buffer]
    remaining: int = size - len(buffer)
    
    while remaining:
        if chunk := await connection.receive():
            chunks.append(chunk.encode())
            remaining =- 1

    return split_scannnig(b"".join(chunks), size)


type Version = str

def parse_request_top(line: str) -> tuple[Method, Path, Version]:
    try:
        method, path, version = line.split(" ", 2)
        return Method(method), Path(path), version.split("/", 1)[1]
    except ValueError:
        raise MalformedMessage(f"Syntax error at: {line}") from ValueError

