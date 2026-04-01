import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.core.scheduler import create_scheduler

settings = get_settings()

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = create_scheduler(settings)
    scheduler.start()
    try:
        yield
    finally:
        try:
            scheduler.shutdown(wait=False)
        except Exception:
            logging.getLogger(__name__).exception("scheduler shutdown failed")


app = FastAPI(title=settings.app_name, lifespan=lifespan)

allow_origins = [o.strip() for o in settings.cors_allow_origins.split(",") if o.strip()] if settings.cors_allow_origins else []

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/health")
def health():
    return {"status": "ok"}
