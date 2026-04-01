from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ParserSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    api_base_url: str = "http://localhost:8000"
    run_headless: bool = True

    list_url: str = "https://www.encar.com/"
    user_agent: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )

    schedule_cron: str = "0 3 * * *"


class CarPayload(BaseModel):
    brand: str
    model: str
    year: int
    mileage: int
    price: int
    image_url: str | None = None
