from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    username = Column(String(50), primary_key=True, index=True)
    password = Column("password", String(128), nullable=False)
