from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from apps.server.auth_service.auth_service import AuthService
from apps.server.auth_service.models import User
from apps.server.deps import (
    AUTH_SERVICE,
    get_postgre_sql_users_database,
    get_auth_service,
)
from apps.server.models import CreateUserRequest, AppendPermissionRequest
from apps.server.ports import UsersDatabase

router = APIRouter()
TAGS = ["users"]


@router.post(
    "/create}",
    tags=TAGS,
    summary="Создание пользователя",
    status_code=status.HTTP_200_OK,
)
async def create(
    request: CreateUserRequest, auth_service: AuthService = Depends(get_auth_service)
) -> None:
    auth_service.create_user(request.username, request.password)


@router.get("/get/{login}", tags=TAGS, summary="Получение пользователя")
async def get(
    username: str,
    users_database: UsersDatabase = Depends(get_postgre_sql_users_database),
    _: User = Depends(AUTH_SERVICE.get_current_user_and_check_permissions()),
) -> User:
    db_user = users_database.get_user(username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return User(username=db_user.username, permissions=db_user.permissions)


@router.post(
    "/append_permission}",
    tags=TAGS,
    summary="Добавление пермишна",
    status_code=status.HTTP_200_OK,
)
async def append_permission(
    request: AppendPermissionRequest,
    users_db: UsersDatabase = Depends(get_postgre_sql_users_database),
) -> None:
    users_db.append_permission(request.username, request.permission)
