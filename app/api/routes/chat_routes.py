from fastapi import APIRouter, HTTPException

from app.schemas.request import ChatRequest
from app.schemas.response import ChatResponse
from services.container import container


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

chat_service = container.chat_service


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        result = chat_service.ask(
            question=request.question,
            top_k=request.top_k,
            gemini_api_key=request.gemini_api_key,
            gemini_model=request.gemini_model,
        )
    except Exception as exception:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate answer: {exception}",
        ) from exception

    return ChatResponse(**result)
