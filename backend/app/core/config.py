from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "million-miles"
    environment: str = "dev"

    database_url: str = "sqlite:///./dev.db"

    cors_allow_origins: str = "*"

    parser_enabled: bool = True
    parser_schedule_cron: str = "0 3 * * *"
    parser_list_url: str = "https://www.encar.com/"
    parser_user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
