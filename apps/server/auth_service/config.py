from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthServiceConfig(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    model_config = SettingsConfigDict(
        env_prefix="AUTH_SERVICE_",
        env_file=".env",
        extra="ignore",
    )
