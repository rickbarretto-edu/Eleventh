from enum import Enum
from typing import Protocol
from uuid import uuid4

import attrs

from eleventh.services.accounts.model import Account

class Creation(Enum):
    SUCCESS = "success"
    USERNAME_TAKEN = "username_taken"
    EMAIL_TAKEN = "email_taken"

type Email = str
type Username = str
type Password = str
type UserID = str

class Accounts(Protocol):

    async def new(
        self, 
        email: Email, 
        username: Username, 
        password: Password
    ) -> Creation:
        ...

    async def authenticate(
        self, 
        email: Email,
        password: Password
    ) -> Account | None:
        ...

class InMemoryAccounts:
    def __init__(self, accounts: list[Account] | None = None) -> None:
        self._usernames: set[Username] = set()
        self._users: dict[Email, Account] = {}

        if accounts:
            for account in accounts:
                self._users[account.email] = account
                self._usernames.add(account.username)

    async def new(self, email: Email, username: Username, password: Password) -> Creation:
        if email in self._users:
            return Creation.EMAIL_TAKEN

        if username in self._usernames:
            return Creation.USERNAME_TAKEN
        
        user = Account(
            uuid=uuid4(),
            email=email,
            username=username,
            hashed_password=hash(password),
        )
        self._users[email] = user
        self._usernames.add(username)
        return Creation.SUCCESS
    
    async def authenticate(self, email: Email, password: Password) -> Account | None:
        if user := self._users.get(email):
            if user.hashed_password == hash(password):
                return user
        return None
