from datetime import datetime, timezone, timedelta

from fastapi import HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from starlette import status

from apps.server.auth.config import AuthServiceConfig
from apps.server.auth.models import User, Permission, AccessTokenPayload
from apps.server.models import BaseRequest
from apps.server.ports import UsersDatabase


class AuthService:
    def __init__(self, config: AuthServiceConfig, users_db: UsersDatabase):
        self.config = config
        self.users_db = users_db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(
        self,
        user: User
    ) -> str:
        now = datetime.now(timezone.utc)
        expire_datetime = now + timedelta(
            minutes=self.config.ACCESS_TOKEN_EXPIRE_MINUTES,
        )

        payload = AccessTokenPayload(
            username=user.username,
            permissions=user.permissions,
            iat=now,
            exp=expire_datetime,
        )

        token = jwt.encode(
            payload.model_dump(),
            self.config.SECRET_KEY,
            algorithm=self.config.ALGORITHM
        )

        return token

    def decode_token(self, token: str) -> AccessTokenPayload:
        try:
            payload = jwt.decode(
                token,
                self.config.SECRET_KEY,
                algorithms=[self.config.ALGORITHM]
            )
            return AccessTokenPayload.model_validate(payload)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)


    def get_current_user_and_check_permissions(self, token: str, required_permission: Permission | None) -> User:
        payload = self.decode_token(token)
        user =  User.model_validate(payload)

        if required_permission and not required_permission in user.permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )

        return user
