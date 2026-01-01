from datetime import datetime
from enum import StrEnum, auto

from pydantic import BaseModel


class Permission(StrEnum):
    READ_USERS_DB = auto()
    WRITE_USERS_DB = auto()


class User(BaseModel):
    username: str
    permissions: list[Permission]


class AccessTokenPayload(BaseModel):
    username: str
    permissions: list[Permission]
    exp: datetime
    iat: datetime
