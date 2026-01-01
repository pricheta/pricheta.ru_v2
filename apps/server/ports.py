from typing import Protocol

from adapters.auth_db.user_db.models import User


class UsersDatabase(Protocol):
    def get_user(self, username: str) -> User: ...

    def create_user(self, username: str, password: str) -> None: ...
