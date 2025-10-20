from __future__ import annotations

import httpx

PEERS: list[str] = []

async def notify_peer(peer: str, new_peer: str):
    """Tell an existing peer about a new node."""
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            _ = await client.post(f"http://{peer}/cluster/join", json={"peer": new_peer})
    except Exception as e:
        print(f"Failed to notify peer {peer}: {e}")

