from datetime import datetime, timezone, timedelta

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from starlette import status

from apps.server.auth_service.config import AuthServiceConfig
from apps.server.auth_service.models import User, Permission, AccessTokenPayload
from apps.server.ports import UsersDatabase


class AuthService:
    def __init__(self, config: AuthServiceConfig, users_db: UsersDatabase):
        self.config = config
        self.users_db = users_db
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")

    def create_access_token(self, user: User) -> str:
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
            algorithm=self.config.ALGORITHM,
        )

        return token

    def decode_token(self, token: str) -> AccessTokenPayload:
        try:
            payload = jwt.decode(
                token, self.config.SECRET_KEY, algorithms=[self.config.ALGORITHM]
            )
            return AccessTokenPayload.model_validate(payload)

        except JWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            ) from exc

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_current_user_and_check_permissions(
        self,
        required_permission: Permission | None = None,
    ):
        def dependency(token: str = Depends(self.oauth2_scheme)) -> User:
            payload = self.decode_token(token)
            user = User(
                username=payload.username,
                permissions=payload.permissions,
            )

            if required_permission and required_permission not in user.permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied",
                )

            return user

        return dependency

    def create_user(self, username: str, password: str) -> None:
        hashed_password = self.hash_password(password)
        self.users_db.create_user(username, hashed_password)
