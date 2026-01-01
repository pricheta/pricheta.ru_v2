from sqlalchemy import Column, String, ARRAY, Enum
from sqlalchemy.ext.declarative import declarative_base

from apps.server.auth_service.models import Permission

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    username = Column(String(50), primary_key=True, index=True)
    password = Column("password", String(128), nullable=False)
    permissions = Column(
        ARRAY(Enum(Permission, native_enum=False)),
        nullable=False,
        default=list
    )