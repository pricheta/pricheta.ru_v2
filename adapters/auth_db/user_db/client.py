from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette import status

from adapters.auth_db.user_db.config import PostgreSQLAuthDBConfig
from adapters.auth_db.user_db.models import User
from apps.server.ports import UsersDatabase


class PostgreSQL(UsersDatabase):
    def __init__(self, config: PostgreSQLAuthDBConfig):
        self.config = config
        self.engine = create_engine(self.config.DATABASE_URL, echo=True)
        self.session_maker = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )


    def get_user(self, username: str) -> User | None:
        session = self.session_maker()
        try:
            return session.query(User).where(User.username == username).first()
        finally:
            session.close()

    def create_user(self, username: str, password: str) -> None:
        session = self.session_maker()
        try:
            user = session.query(User).where(User.username == username).first()

            if user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"User '{username}' already exists",
                )

            user = User(
                username=username,
                password=password,
            )
            session.add(user)
            session.commit()
        finally:
            session.close()
