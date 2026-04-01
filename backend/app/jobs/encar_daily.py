import asyncio
import logging

from sqlalchemy.orm import Session

from app.core.config import Settings
from app.db.session import SessionLocal
from app.parser.encar_parser import scrape_encar
from app.schemas.car import CarCreate
from app.services.car_service import CarService

logger = logging.getLogger(__name__)


def _persist_cars(parsed, service: CarService) -> int:
    db: Session = SessionLocal()
    try:
        created = 0
        for c in parsed:
            payload = CarCreate(
                brand=c.brand,
                model=c.model,
                year=c.year or 0,
                mileage=c.mileage or 0,
                price=c.price or 0,
                image_url=c.image_url,
            )
            service.create(db=db, payload=payload)
            created += 1
        return created
    finally:
        db.close()


async def run_encar_job(settings: Settings) -> None:
    logger.info("encar_job started")

    try:
        parsed = await scrape_encar(
            list_url=settings.parser_list_url,
            user_agent=settings.parser_user_agent,
            headless=True,
            max_items=50,
        )

        service = CarService()
        created = await asyncio.to_thread(_persist_cars, parsed, service)
        logger.info("encar_job finished created=%s", created)

    except Exception:
        logger.exception("encar_job failed")
