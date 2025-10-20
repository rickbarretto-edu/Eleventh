from cyclopts import App
import uvicorn

from node.peers import Peer
from claim.api import app as claim_app

__all__ = ["app"]

app = App("claim", help="Rewarding Claim Service.")

@app.default
def main(peer: Peer = Peer()) -> None:
    """Start the Claim service with specified peer configuration."""

    uvicorn.run(
        claim_app,
        host=peer.host,
        port=peer.port,
    )
