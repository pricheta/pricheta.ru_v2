from typing import Protocol

from apps.server.auth.models import User


class UsersDatabase(Protocol):
    def get_user(self, username: str) -> User: ...

    def create_user(self, username: str, password: str) -> None: ...
