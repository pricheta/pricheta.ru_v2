from apps.server.auth.models import User
from apps.server.models import BaseRequest
from apps.server.auth.ports import AuthDB


class AuthService:
    def __init__(self, auth_db: AuthDB):
        self.auth_db = auth_db

    def get_current_user(self, request: BaseRequest) -> User:
        username = request.credentials.username
        password = request.credentials.password
        return self.auth_db.authenticate_user(username, password)
