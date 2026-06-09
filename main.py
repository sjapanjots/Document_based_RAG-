from fastapi import FastAPI

from app.api.routes import api_router
from core.config import settings
from core.logger import logger

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)


@app.on_event("startup")
async def startup_event() -> None:
    logger.info("Application started successfully")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    logger.info("Application shutdown")


app.include_router(
    api_router,
    prefix=settings.API_PREFIX
)