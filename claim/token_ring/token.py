import asyncio
import httpx
from fastapi import BackgroundTasks

from claim.token_ring.model import State


async def receive_token(state: State, background: BackgroundTasks):
    """Receive a token ring in background."""

    async with state.token_lock:
        if not state.config:
            return {"error": "Not configured"}
        state.config.has_token = True
        background.add_task(handle_token, state)
        return {"status": "token_received", "node_id": state.config.node_id}


async def handle_token(state: State):
    """Perform queued operations then pass token."""

    assert state.config
    print(f"[Node {state.config.node_id}] Holding token.")
    await asyncio.sleep(0.3)

    for action, value in state.pending_ops:
        match action:
            case "store":
                state.shared_list.append(value)
                print(
                    f"[Node {state.config.node_id}] Stored '{value}'. List={state.shared_list}"
                )
            case "claim" if state.shared_list:
                removed = state.shared_list.pop(0)
                print(
                    f"[Node {state.config.node_id}] Discarted '{removed}'. List={state.shared_list}"
                )
            case _:
                pass

    state.pending_ops.clear()
    await asyncio.sleep(0.2)
    await pass_token(state)


async def pass_token(state: State):
    if not state.config:
        return

    async with httpx.AsyncClient() as client:
        try:
            _ = await client.post(f"{state.config.next_node}/receive_token", timeout=5)
            print(
                f"[Node {state.config.node_id}] Passed token → {state.config.next_node}"
            )
            state.config.has_token = False
        except Exception as e:
            print(f"[Node {state.config.node_id}] Failed to pass token: {e}")


async def token_watchdog(state: State):
    while True:
        await asyncio.sleep(5)
        if state.config and state.config.has_token:
            await pass_token(state)
