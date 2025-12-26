from functools import lru_cache

from adapters.auth_db.user_db.client import PostgreSQL
from adapters.auth_db.user_db.config import PostgreSQLAuthDBConfig
from apps.server.auth.auth_service import AuthService
from apps.server.auth.config import AuthServiceConfig


@lru_cache(maxsize=1)
def get_postgre_sql_users_database() -> PostgreSQL:
    postgre_sql_auth_db_config = PostgreSQLAuthDBConfig()
    return PostgreSQL(postgre_sql_auth_db_config)


@lru_cache(maxsize=1)
def get_auth_service() -> AuthService:
    config = AuthServiceConfig()
    postgre_sql_auth_db = get_postgre_sql_users_database()
    return AuthService(config, postgre_sql_auth_db)


AUTH_SERVICE = get_auth_service()
USERS_DATABASE = get_postgre_sql_users_database()
