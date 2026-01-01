from typing import Protocol

from adapters.auth_db.user_db.models import User
from apps.server.auth_service.models import Permission


class UsersDatabase(Protocol):
    def get_user(self, username: str) -> User: ...

    def create_user(self, username: str, password: str) -> None: ...

    def append_permission(self, username: str, permission: Permission) -> None: ...
