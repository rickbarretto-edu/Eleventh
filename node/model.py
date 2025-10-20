from __future__ import annotations
from typing_extensions import Literal

import attrs
import httpx


@attrs.define
class Cluster:
    nodes: set[str] = attrs.field(factory=set)

    async def join_cluster(self, cluster_node: str, peer: str):
        async with httpx.AsyncClient(timeout=3, base_url=cluster_node) as client:
            response = await client.post("/cluster/join", json={ "peer": peer })
            nodes: list[str] = response.json()["nodes"]
            self.nodes.union(set(nodes))

    def on_add(self, peer: str):
        """On new requested to be added to the current Node."""
        self.nodes.add(peer)
        
    async def on_join_cluster(self, peer: str):
        """On requested to be added to the cluster."""
        for other in self.nodes:
            async with httpx.AsyncClient(timeout=3, base_url=other) as client:
               _ = await client.post("/cluster/node/add", json={ "peer": peer })
              
        self.nodes.add(peer)
