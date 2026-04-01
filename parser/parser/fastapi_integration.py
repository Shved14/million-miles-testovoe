from fastapi import APIRouter, Depends

from parser.config import ParserSettings
from parser.encar_scraper import scrape_encar
from parser.sink_api import save_to_db


def get_settings() -> ParserSettings:
    return ParserSettings()


def create_router() -> APIRouter:
    router = APIRouter(prefix="/parser", tags=["parser"])

    @router.get("/encar")
    async def parse_encar(max_items: int = 20, settings: ParserSettings = Depends(get_settings)):
        cars = await scrape_encar(settings=settings, max_items=max_items)
        return [c.model_dump() for c in cars]

    @router.post("/encar/save")
    async def parse_and_save_encar(max_items: int = 20, settings: ParserSettings = Depends(get_settings)):
        cars = await scrape_encar(settings=settings, max_items=max_items)
        created = await save_to_db(api_base_url=settings.api_base_url, cars=cars)
        return {"created": created}

    return router
