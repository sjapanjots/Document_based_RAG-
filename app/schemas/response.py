from pydantic import BaseModel


class UploadResponse(BaseModel):
    filename: str
    page_count: int
    character_count: int
    chunk_count: int


class SourceChunk(BaseModel):
    text: str
    score: float
    metadata: dict


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]

