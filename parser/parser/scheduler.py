from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from parser.config import ParserSettings
from parser.encar_scraper import scrape_encar
from parser.sink_api import push_to_api


def run_once() -> int:
    settings = ParserSettings()
    cars = scrape_encar(settings=settings)
    return push_to_api(api_base_url=settings.api_base_url, cars=cars)


def run_scheduler() -> None:
    settings = ParserSettings()

    scheduler = BlockingScheduler(timezone="UTC")
    trigger = CronTrigger.from_crontab(settings.schedule_cron)

    def job():
        cars = scrape_encar(settings=settings)
        push_to_api(api_base_url=settings.api_base_url, cars=cars)

    scheduler.add_job(job, trigger=trigger, id="encar_daily")
    scheduler.start()
