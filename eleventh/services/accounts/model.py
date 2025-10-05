from uuid import UUID
import attrs


@attrs.frozen(slots=True)
class Account:
    uuid: UUID
    email: str
    username: str
    hashed_password: int
    is_active: bool = True
