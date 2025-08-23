from __future__ import annotations

import urllib.parse as url

import attrs

__all__ = [
    "JsonValue",
    "Target",
]


type JsonValue = dict[str, str | list[str] | JsonValue]


@attrs.frozen
class Target:
    _raw: str

    @property
    def path(self) -> str:
        return self._url.path or "/" 

    @property
    def query(self) -> JsonValue:
        return {
            key: (value[0] if len(value) == 1 else value) 
            for key, value in url.parse_qs(self._url.query).items()
        }

    @property
    def _url(self) -> url.ParseResult:
        return url.urlparse(self._raw)

    def __str__(self) -> str:
        return self._raw