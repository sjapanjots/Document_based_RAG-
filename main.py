from fastapi import FastAPI

from app.api.routes.router import api_router
from core.config import settings
from core.logger import get_logger


logger = get_logger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)


@app.on_event("startup")
async def startup_event() -> None:
    logger.info("Application Started")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    logger.info("Application Stopped")


app.include_router(
    api_router,
    prefix="/api/v1"
)