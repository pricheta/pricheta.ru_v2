from pydantic import BaseModel

from apps.server.auth_service.models import Permission


class CreateUserRequest(BaseModel):
    username: str
    password: str


class AppendPermissionRequest(BaseModel):
    username: str
    permission: Permission


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
