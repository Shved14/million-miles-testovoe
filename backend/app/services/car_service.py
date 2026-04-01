from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.car import Car
from app.schemas.car import CarCreate


class CarService:
    def list(self, db: Session, limit: int = 100, offset: int = 0) -> list[Car]:
        stmt = select(Car).order_by(desc(Car.created_at)).limit(limit).offset(offset)
        return list(db.execute(stmt).scalars().all())

    def create(self, db: Session, payload: CarCreate) -> Car:
        car = Car(
            brand=payload.brand,
            model=payload.model,
            year=payload.year,
            mileage=payload.mileage,
            price=payload.price,
            image_url=str(payload.image_url) if payload.image_url else None,
        )
        db.add(car)
        db.commit()
        db.refresh(car)
        return car
