from quickapi import tcp


__all__ = [
    "body",
    "frame"
]


async def frame(connection: tcp.Connection, current_buffer: str):
    empty_line = "\r\n\r\n"
    buffer = list(current_buffer)

    while empty_line not in buffer:
        if (chunk := await connection.receive()):
            buffer += chunk
        else:
            return None, "".join(buffer)

    head, tail = "".join(buffer).split(empty_line, 1)
    return head, tail


def _to_str_safe(content: bytes) -> str:
    return content.decode("replace")


def _split_scannnig(content: bytes, size: int): 
    return (
        _to_str_safe(content[:size]), 
        _to_str_safe(content[size:])
    )


async def body(connection: tcp.Connection, prev_buffer: str, size: int) -> tuple[str, str]:
    buffer: bytes = prev_buffer.encode()
    if len(buffer) >= size:
        return _split_scannnig(buffer, size)
    
    return await _large_body(connection, buffer, size)


async def _large_body(connection: tcp.Connection, buffer: bytes, size: int) -> tuple[str, str]:
    chunks: list[bytes] = [buffer]
    remaining: int = size - len(buffer)
    
    while remaining:
        if chunk := await connection.receive():
            chunks.append(chunk.encode())
            remaining =- 1

    return _split_scannnig(b"".join(chunks), size)
