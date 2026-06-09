from fastapi import APIRouter

from app.api.routes.chat_routes import router as chat_router
from api.routes.health_routes import router as health_router
from api.routes.upload_routes import router as upload_router


api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(upload_router)
api_router.include_router(chat_router)