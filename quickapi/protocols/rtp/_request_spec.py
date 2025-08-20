import pytest

from quickapi.protocols.generic import Body, Json, PlainText, Xml
from quickapi.protocols.generic.request import Path, Method

from quickapi.protocols.rtp.request import RTPRequest

def test_request_format():
    body = Json(
        '{\n'
        '    "protocol": "Rick Transfer Protocol",\n'
        '    "version": "1.0",\n'
        '    "abbr": "RTP",\n'
        '}'
    )
    req = RTPRequest(method=Method.Post, path=Path("/protocols/create"), body=body)

    expected = (
        "POST /protocols/create RTP/1.0\n"
        f"size: {len(body)}\n"
        f"type: {body.type}\n"
        f"{body}"
    )

    assert expected == str(req)


def test_body_content():
    body = Body("hello", "any")
    assert "hello" == body.content
    assert "hello" == str(body)
    assert b"hello" == body.as_bytes()


@pytest.mark.parametrize("cls,expected", [
    (Json, "json"),
    (PlainText, "text"),
    (Xml, "xml"),
])
def test_body_types(cls, expected):
    content = "hello"
    body = cls(content)
    assert body.type == expected


def test_body_size():
    body = Body("hello", "any")
    expected = len("hello".encode("utf-8"))

    assert expected == body.bytes 
    assert expected == len(body)


def test_path():
    path = Path("/test/path")
    assert path.value == "/test/path"
    assert path.value == str(path)


def test_method():
    assert "GET" == str(Method.get)
    assert "POST" == str(Method.Post)
    assert "BUY" == str(Method("Buy"))
