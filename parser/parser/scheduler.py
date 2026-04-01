import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from parser.config import ParserSettings
from parser.encar_scraper import scrape_encar
from parser.sink_api import save_to_db


async def run_once() -> int:
    settings = ParserSettings()
    cars = await scrape_encar(settings=settings)
    return await save_to_db(api_base_url=settings.api_base_url, cars=cars)


async def run_scheduler() -> None:
    settings = ParserSettings()

    scheduler = AsyncIOScheduler(timezone="UTC")
    trigger = CronTrigger.from_crontab(settings.schedule_cron)

    async def job():
        cars = await scrape_encar(settings=settings)
        await save_to_db(api_base_url=settings.api_base_url, cars=cars)

    scheduler.add_job(job, trigger=trigger, id="encar_daily")
    scheduler.start()
    await asyncio.Event().wait()
