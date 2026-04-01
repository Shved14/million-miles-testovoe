from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.car import CarCreate, CarOut
from app.services.car_service import CarService

router = APIRouter(prefix="/cars", tags=["cars"])

service = CarService()


@router.get("", response_model=list[CarOut])
def list_cars(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    return service.list(db=db, limit=limit, offset=offset)


@router.post("", response_model=CarOut, status_code=201)
def create_car(payload: CarCreate, db: Session = Depends(get_db)):
    return service.create(db=db, payload=payload)
