from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)
    top_k: int | None = Field(default=None, ge=1, le=10)
    gemini_api_key: str | None = Field(default=None)
    gemini_model: str | None = Field(default=None)
