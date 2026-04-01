from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ParserSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    api_base_url: str = "http://localhost:8000"
    run_headless: bool = True

    schedule_cron: str = "0 3 * * *"  # daily at 03:00


class CarPayload(BaseModel):
    brand: str
    model: str
    year: int
    mileage: int
    price: int
    image_url: str | None = None
