from cyclopts import App
import uvicorn

from node.cli import Peer
from decks.api import app as deck_app

__all__ = ["app"]

app = App("decks", help="Deck Management Service.")

@app.default
def main(peer: Peer = Peer()) -> None:
    """Start the Deck service with specified peer configuration."""

    uvicorn.run(
        deck_app,
        host=peer.host,
        port=peer.port,
    )
