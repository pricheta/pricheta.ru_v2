from pydantic import BaseModel

from apps.server.auth.models import Credentials


class BaseRequest(BaseModel):
    credentials: Credentials


class CreateUserRequest(BaseModel):
    username: str
    password: str
