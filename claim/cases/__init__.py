from typing import Literal
from pydantic import BaseModel
from claim.token_ring.model import State


class StoreSuccess(BaseModel):
    status: Literal["success"] = "success"


class StoreQueued(BaseModel):
    message: str
    status: Literal["queued"] = "queued"


class StoreFail(BaseModel):
    message: str
    status: Literal["fail"] = "fail"


type StoreResponse = StoreSuccess | StoreQueued | StoreFail


async def store(state: State, card: object) -> StoreResponse:
    if not state.is_configured:
        return StoreFail(message="Not configured")

    assert state.config
    if state.config.has_token:
        state.shared_list.append(card)
        print(
            f"[Node {state.config.node_id}] Direct append '{card}'. List={state.shared_list}"
        )
        return StoreSuccess()
    else:
        state.pending_ops.append(("store", card))
        print(f"[Node {state.config.node_id}] Queued store({card})")
        return StoreQueued(message=f"Store({card}) queued.")


class ClaimSuccess(BaseModel):
    claim: list[dict]
    status: Literal["success"] = "success"


class ClaimFail(BaseModel):
    message: str
    status: Literal["fail"] = "fail"


type ClaimResponse = ClaimSuccess | ClaimFail


async def claim(state: State, amount: int) -> ClaimResponse:
    if not state.is_configured:
        return ClaimFail(message="Not configured")

    assert state.config
    while not state.config.has_token:
        pass

    if not state.shared_list:
        return ClaimFail(message="empty list")

    try:
        value = state.shared_list.pop(amount)
        print(
            f"[Node {state.config.node_id}] Direct pop '{value}'. List={state.shared_list}"
        )
        return ClaimSuccess(claim=value)
    except Exception as e:
        return ClaimFail(message=str(e))
