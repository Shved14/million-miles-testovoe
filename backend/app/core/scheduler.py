import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.config import Settings
from app.jobs.encar_daily import run_encar_job

logger = logging.getLogger(__name__)


def create_scheduler(settings: Settings) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="UTC")

    if settings.parser_enabled:
        trigger = CronTrigger.from_crontab(settings.parser_schedule_cron)
        scheduler.add_job(
            run_encar_job,
            trigger=trigger,
            id="encar_daily",
            kwargs={"settings": settings},
            max_instances=1,
            coalesce=True,
            misfire_grace_time=3600,
        )
        logger.info("scheduler job registered id=encar_daily cron=%s", settings.parser_schedule_cron)
    else:
        logger.info("scheduler disabled")

    return scheduler
