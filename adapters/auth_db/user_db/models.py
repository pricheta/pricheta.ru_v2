from sqlalchemy import Column, String, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.mutable import MutableList


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    username = Column(String(50), primary_key=True, index=True)
    password = Column("password", String(128), nullable=False)
    permissions = Column(
        MutableList.as_mutable(ARRAY(String)), nullable=False, default=list
    )
