import attrs
from httpx import URL

from node.client.broadcast import Broadcast

type Alive = bool
type PeerID = str

@attrs.frozen
class Peer:
    id: PeerID
    url: URL

@attrs.define
class StaticCluster:
    current: PeerID
    all: list[Peer] = attrs.field(factory=list)

    @property
    def client(self) -> Broadcast:
        return Broadcast(peer.url for peer in self.others)
    
    @property
    def others(self) -> list[Peer]:
        return [peer for peer in self.all if peer.id != self.current]
  