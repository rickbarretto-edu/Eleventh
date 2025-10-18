from typing import Annotated

import attrs
from cyclopts import Parameter

__all__ = ["Peer"]

LOCALHOST = "127.0.0.1"
PUBLIC_HOST = "0.0.0.0"
ANY_PORT = 0

@attrs.frozen()
class Peer:
    """Command line arguments for peer configuration."""
    host: Annotated[str, Parameter(name="--host", help="The peer host address")] = LOCALHOST
    port: Annotated[int, Parameter(name="--port", help="The peer port number")] = ANY_PORT
    localhost: Annotated[bool, Parameter(name="--localhost", help=f"Set host to {LOCALHOST}")] = False
    production: Annotated[bool, Parameter(name="--production", help=f"Set host to {PUBLIC_HOST}")] = False

    def __attrs_post_init__(self) -> None:
        if self.host == LOCALHOST:
            if self.localhost:
                object.__setattr__(self, "host", LOCALHOST)
            elif self.production:
                object.__setattr__(self, "host", PUBLIC_HOST)
