from typing import Protocol
from uuid import UUID

from eleventh.login.model import UserID, UserLogin
from eleventh.login.repository.sqlite import UsersInSQLite

__all__ = [
    "Users",
    "UsersInSQLite"
]

class Users(Protocol):

    def new(self, login: UserLogin) -> UserID | None:
        ...

    def auth(self, login: UserLogin) -> UserID | None:
        ...
    
    def by_id(self, id: UUID) -> UserID | None:
        ...

    def by_name(self, name: str) -> UserID | None:
        ...
