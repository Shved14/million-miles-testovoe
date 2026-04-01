from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class CarCreate(BaseModel):
    brand: str = Field(min_length=1, max_length=100)
    model: str = Field(min_length=1, max_length=150)
    year: int
    mileage: int
    price: int
    image_url: HttpUrl | None = None


class CarOut(BaseModel):
    id: int
    brand: str
    model: str
    year: int
    mileage: int
    price: int
    image_url: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
