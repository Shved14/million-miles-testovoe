from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "million-miles"
    environment: str = "dev"

    database_url: str = "sqlite:///./dev.db"

    cors_allow_origins: str = "*"


@lru_cache
def get_settings() -> Settings:
    return Settings()
