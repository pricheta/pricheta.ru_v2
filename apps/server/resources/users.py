from fastapi import APIRouter, Depends


from apps.server.auth.models import User
from apps.server.deps import AUTH_SERVICE, get_postgre_sql_users_database
from apps.server.models import CreateUserRequest
from apps.server.ports import UsersDatabase

router = APIRouter()
TAGS = ["users"]


@router.post("/create}", tags=TAGS, summary="Создание пользователя")
async def create(
    request: CreateUserRequest,
    users_database: UsersDatabase = Depends(get_postgre_sql_users_database),
) -> None:
    username = request.username
    password = request.password
    users_database.create_user(username, password)


@router.post("/get/{login}", tags=TAGS, summary="Получение пользователя")
async def get(
    username: str,
    users_database: UsersDatabase = Depends(get_postgre_sql_users_database),
    _: User = Depends(AUTH_SERVICE.get_current_user),
) -> User:
    return users_database.get_user(username)
