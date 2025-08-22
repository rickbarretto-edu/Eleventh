import pytest

from quickapi.http.request.parse import from_connection

class FakeConnection:
    def __init__(self, messages):
        self._messages = messages
        self._index = 0

    async def receive(self):
        if self._index < len(self._messages):
            msg = self._messages[self._index]
            self._index += 1
            return msg
        return ""


@pytest.mark.asyncio
async def test_simple_get():
    buffer = "GET / HTTP/1.0\r\nHost: example.com\r\n\r\n"
    connection = FakeConnection([])
    request, remainder = await from_connection(connection, buffer) # pyright: ignore[reportArgumentType]

    assert request
    assert str(request.method) == "GET"
    assert str(request.target) == "/"
    assert request.body.content == ""
    assert remainder == ""


@pytest.mark.asyncio
async def test_post_with_body_inline():
    buffer = (
        "POST /submit HTTP/1.0\r\n"
        "Host: example.com\r\n"
        "Content-Length: 11\r\n"
        "Content-Type: text/plain\r\n"
        "\r\n"
        "Hello WorldExtraData"
    )
    connection = FakeConnection([])
    request, remainder = await from_connection(connection, buffer) # pyright: ignore[reportArgumentType]

    assert request
    assert str(request.method) == "POST"
    assert str(request.target) == "/submit"
    assert request.body.content == "Hello World"
    assert remainder == "ExtraData"


@pytest.mark.asyncio
async def test_post_with_body_chunks():
    head = (
        "POST /upload HTTP/1.0\r\n"
        "Host: example.com\r\n"
        "Content-Length: 20\r\n"
        "Content-Type: text/plain\r\n"
        "\r\n"
    )
    connection = FakeConnection(["Hello ", "World ", "and more!"])
    request, remainder = await from_connection(connection, head) # pyright: ignore[reportArgumentType]
    
    assert request
    assert request.body.content == "Hello World and more"
    assert remainder == "!"


@pytest.mark.asyncio
async def test_missing_content_length_defaults_zero():
    buffer = "GET /foo HTTP/1.0\r\nHost: test\r\n\r\nSOMEEXTRA"
    connection = FakeConnection([])
    request, remainder = await from_connection(connection, buffer) # pyright: ignore[reportArgumentType]
    
    assert request
    assert request.body.content == ""
    assert remainder == "SOMEEXTRA"


@pytest.mark.asyncio
async def test_invalid_request_line():
    bad_request = "BADREQUEST\r\nHost: x\r\n\r\n"
    connection = FakeConnection([])
    with pytest.raises(ValueError):
        await from_connection(connection, bad_request) # pyright: ignore[reportArgumentType]


@pytest.mark.asyncio
async def test_unsupported_version():
    bad_request = "GET / HTTP/2.0\r\nHost: x\r\n\r\n"
    connection = FakeConnection([])
    with pytest.raises(ValueError):
        await from_connection(connection, bad_request) # pyright: ignore[reportArgumentType]