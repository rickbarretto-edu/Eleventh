from quickapi import tcp


__all__ = [
    "body",
    "frame"
]


async def frame(connection: tcp.Connection, current_buffer: str) -> tuple[str | None, str]:
    """Scan until the end of the headers.

    Returns
    -------
        (head: str, tail: str): For complete message.
        (head: None, buffer: str): For incomplete message.
    """
    end_of_header = "\r\n\r\n"
    buffer = current_buffer

    while end_of_header not in buffer:
        if (chunk := await connection.receive()):
            buffer += chunk
        else:
            return None, buffer

    head, tail = buffer.split(end_of_header, 1)
    return head, tail


def _split_scanning(content: str, size: int) -> tuple[str, str]:
    """Split body into (consumed, remainder).
    
    Returns
    -------
    (consumed: str, remainder: str)
    """
    return content[:size], content[size:]


async def body(connection: tcp.Connection, prev_buffer: str, size: int) -> tuple[str, str]:
    """Read body of fixed size.
    
    Returns
    -------
    Returns parsed tokens: (consumed, remainder)
    """
    buffer = prev_buffer
    if len(buffer) >= size:
        return _split_scanning(buffer, size)

    return await _large_body(connection, buffer, size)


async def _large_body(connection: tcp.Connection, buffer: str, size: int) -> tuple[str, str]:
    """Read a body that is larger than the buffer.
    
    Returns
    -------
    Returns parsed tokens: (consumed, remainder)
    """
    chunks: list[str] = [buffer]
    remaining: int = size - len(buffer)

    while remaining > 0:
        if chunk := await connection.receive():
            chunks.append(chunk)
            remaining -= len(chunk)
        else:
            break

    return _split_scanning("".join(chunks), size)
