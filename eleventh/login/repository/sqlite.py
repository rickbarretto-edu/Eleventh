import contextlib
from functools import cached_property
import sqlite3
from uuid import UUID
import attrs

from eleventh.login.model import UserID, UserLogin

__all__ = [
    "UsersInSQLite"
]

@attrs.frozen
class UsersInSQLite:
    path: str

    @cached_property
    def db(self) -> sqlite3.Connection:
        db = sqlite3.connect(self.path)
        db.execute("PRAGMA foreign_keys = ON")
        return db

    def __attrs_post_init__(self):
        self.db.execute("""
            create table if not exists Users (
                Id       text primary key,
                Name     text unique not null,
                Password text not null
            )
        """)
        self.db.commit()

    def new(self, login: UserLogin) -> UserID | None:
        with contextlib.suppress(sqlite3.IntegrityError):
            user_id = UserID()
            self.db.execute(
                "insert into Users (Id, Name, Password) values (?, ?, ?)",
                (user_id, login.username, login.password),
            )
            self.db.commit()
            return user_id
        
        return None

    def auth(self, login: UserLogin) -> UserID | None:
        select = "select Id from Users where Name = ? and Password = ?"
        values = login.username, login.password
        
        if row := self.db.execute(select, values).fetchone():
            return UserID(UUID(row[0]))
        else:
            return None

    def by_id(self, id: UUID) -> UserID | None:
        select = "select Id from Users where Id = ?"
        values = (str(id),)
        
        if row := self.db.execute(select,values).fetchone():
            return UserID(UUID(row[0]))
        else:
            return None

    def by_name(self, name: str) -> UserID | None:
        """Find user by username."""
        select = "select Id from Users where Name = ?"
        values = (name,)

        if row := self.db.execute(select, values).fetchone():
            return UserID(UUID(row[0]))
        else:
            return None
