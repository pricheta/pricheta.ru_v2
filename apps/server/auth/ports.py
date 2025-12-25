from typing import Protocol

from apps.server.auth.models import User


class AuthDB(Protocol):
    def hash_password(self, password: str) -> str: ...

    def authenticate_user(self, username: str, password: str) -> User: ...
