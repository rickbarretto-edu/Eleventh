# test_response.py
import pytest
from .response import Body, Response, Status, Html, Json, PlainText, Xml


def test_response_format():
    body = Html(
        "<section>\n"
        "    Created Protocol: <strong>Rick Transfer Protocol v1.0 (RTP/1.0)</strong>\n"
        "</section>"
    )
    resp = Response(status=Status.Ok, body=body)

    expected = (
        "RTP/1.0 200 Ok\n"
        f"size: {len(body)}\n"
        f"type: html\n"
        "\n"
        f"{body}"
    )

    assert expected == str(resp)



def test_body_content():
    body = Body("hello", "any")

    assert "hello" == str(body)
    assert b"hello" == body.as_bytes()


@pytest.mark.parametrize("cls,expected", [
    (Html, "html"),
    (Json, "json"),
    (PlainText, "text"),
    (Xml, "xml"),
])
def test_body_type(cls, expected):
    body = cls("hello")
    assert expected == body.type


def test_body_size():
    body = Body("hello", "any")

    expected = len("hello".encode("utf-8"))
    assert expected == body.bytes
    assert expected == len(body)


def test_status():
    assert 200 == Status.Ok.code
    assert "Ok" == Status.Ok.reason
    assert "200 Ok" == str(Status.Ok)

    assert 400 == Status.NotFound.code
    assert "Not Found" == Status.NotFound.reason
    assert "400 Not Found" == str(Status.NotFound)
