from pydantic import BaseModel


class User(BaseModel):
    username: str


class Credentials(BaseModel):
    username: str
    password: str
