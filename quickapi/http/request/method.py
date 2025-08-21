"""Define available HTTP methods"""

from typing import Self

import attrs


@attrs.frozen
class HTTPMethod:
    value: str = attrs.field(converter=str.upper)

    def __str__(self) -> str:
        return self.value

    @classmethod
    def get(cls) -> Self:
        """Retrieve a resource."""
        return cls("GET")

    @classmethod
    def head(cls) -> Self:
        """Bodyless GET."""
        return cls("HEAD")

    @classmethod
    def options(cls) -> Self:
        """Inquire about communication options for resource."""
        return cls("OPTIONS")

    @classmethod
    def post(cls) -> Self:
        """Create a resource."""
        return cls("POST")

    @classmethod
    def put(cls) -> Self:
        """Replace a resource entirely."""
        return cls("PUT")

    @classmethod
    def patch(cls) -> Self:
        """Partially modify a resource."""
        return cls("PATCH")

    @classmethod
    def delete(cls) -> Self:
        """Remove a resource"""
        return cls("DELETE")

    @classmethod
    def trace(cls) -> Self:
        """Loop-back test for debugging."""
        return cls("TRACE")

    @classmethod
    def connect(cls) -> Self:
        """Establish a tunnel."""
        return cls("CONNECT")
