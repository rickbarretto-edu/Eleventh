from hashlib import sha512
from uuid import UUID, uuid4

import attrs

@attrs.frozen
class UserID(UUID):
    id: UUID = attrs.field(factory=uuid4)


@attrs.frozen
class User:
    id: UserID
    username: str
    hashed_password: str


@attrs.frozen
class UserLogin:
    username: str
    _password: str = attrs.field(repr=False)

    @property
    def password(self) -> str:
        return sha512(self._password.encode()).hexdigest()

