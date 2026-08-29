from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_VERSION: str = "0.0.1"
    FASTAPI_WORKERS: int = 1
    ENV: str = "development"

    # DATABASE
    DB_HOST: str | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_NAME: str | None = None
    LIMIT_DEFAULT_VALUE: int = 1000
    
    SYSADMIN_USERS: str = ("anjeumi@gmail.com")
    
    model_config = SettingsConfigDict(env_file=(".env", ".env.local"), env_file_encoding="utf-8")

settings = Settings()