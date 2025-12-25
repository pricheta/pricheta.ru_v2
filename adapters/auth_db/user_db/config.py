from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgreSQLAuthDBConfig(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_prefix="POSTGRE_SQL_AUTH_",
        env_file=".env",
    )
