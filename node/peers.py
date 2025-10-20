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

async def join_peers(new_peer: str, existing: list[str] | None = None):
    """Join an existing cluster if provided, or start fresh."""
    global PEERS
    if existing:
        for peer in existing:
            await notify_peer(peer, new_peer)
        PEERS.extend(existing)
    if new_peer not in PEERS:
        PEERS.append(new_peer)
