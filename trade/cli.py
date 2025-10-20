from cyclopts import App
import uvicorn

from node.peers import Peer
from trade.api import app as trade_app

__all__ = ["app"]

app = App("trade", help="Manage card trading operations and peer connections.")

@app.default
def main(peer: Peer = Peer()) -> None:
    """Start the Trade service with specified peer configuration."""

    uvicorn.run(
        trade_app,
        host=peer.host,
        port=peer.port,
    )
