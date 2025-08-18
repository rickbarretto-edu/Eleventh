# test_request.py
import pytest
from .request import Body, Request, Path, Method, Json, PlainText, Xml


def test_request_format():
    body = Json(
        '{\n'
        '    "protocol": "Rick Transfer Protocol",\n'
        '    "version": "1.0",\n'
        '    "abbr": "RTP",\n'
        '}'
    )
    req = Request(method=Method.Post, path=Path("/protocols/create"), body=body)

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
    assert "GET" == Method.Get
    assert "POST" == Method.Post

    assert "GET" == Method.Get.value
    assert "POST" == Method.Post.value

    assert "GET" == str(Method.Get)
    assert "POST" == str(Method.Post)
