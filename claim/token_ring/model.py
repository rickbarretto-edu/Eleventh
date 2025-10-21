import asyncio
from typing import Literal

import attrs
from pydantic import BaseModel

class Config(BaseModel):
    node_id: int
    next_node: str
    has_token: bool = False
    
type Action = Literal["claim", "store"]

@attrs.define
class State:
    config: Config | None = None
    token_lock: asyncio.Lock = attrs.field(factory=asyncio.Lock)
    shared_list: list[object] = attrs.field(factory=list)
    pending_ops: list[tuple[Action, object]] = attrs.field(factory=list)

    @property
    def is_configured(self) -> bool:
        return self.config is not None


state = State()
