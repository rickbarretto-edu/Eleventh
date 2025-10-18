from cyclopts import App
import uvicorn

from node.cli import Peer
from rewards.api import app as rewards_app

__all__ = ["app"]

app = App("rewards", help="Rewarding Generation Service.")

@app.default
def main(peer: Peer = Peer()) -> None:
    """Start the Rewards service with specified peer configuration."""

    uvicorn.run(
        rewards_app,
        host=peer.host,
        port=peer.port,
    )
