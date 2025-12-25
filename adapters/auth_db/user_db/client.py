from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette import status

from passlib.context import CryptContext

from adapters.auth_db.user_db.config import PostgreSQLAuthDBConfig
from adapters.auth_db.user_db.models import User as UserDB
from apps.server.auth.models import User
from apps.server.auth.ports import AuthDB
from apps.server.ports import UsersDatabase


class PostgreSQL(AuthDB, UsersDatabase):
    def __init__(self, config: PostgreSQLAuthDBConfig):
        self.config = config
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.engine = create_engine(self.config.DATABASE_URL, echo=True)
        self.session_maker = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def authenticate_user(self, username: str, password: str) -> User:
        session = self.session_maker()
        try:
            user_db = session.query(UserDB).where(UserDB.username == username).first()

            if not user_db:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Wrong username",
                )

            if not self.pwd_context.verify(password, user_db.password):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Wrong password",
                )

            return User(
                username=user_db.username,
            )
        finally:
            session.close()

    def get_user(self, username: str) -> User:
        session = self.session_maker()
        try:
            user_db = session.query(UserDB).where(UserDB.username == username).first()
            if not user_db:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User '{username}' not found",
                )
            return User(
                username=user_db.username,
            )
        finally:
            session.close()

    def create_user(self, username: str, password: str) -> None:
        session = self.session_maker()
        try:
            user_db = session.query(UserDB).where(UserDB.username == username).first()
            if user_db:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"User '{username}' already exists",
                )

            user_db = UserDB(
                username=username,
                password=self.hash_password(password),
            )
            session.add(user_db)
            session.commit()
        finally:
            session.close()
