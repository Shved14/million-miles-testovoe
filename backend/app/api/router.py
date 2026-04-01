from fastapi import APIRouter

from app.api.routes.cars import router as cars_router

api_router = APIRouter()

api_router.include_router(cars_router)
