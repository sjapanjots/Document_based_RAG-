from pydantic import BaseModel


class UploadResponse(BaseModel):

    filename: str

    page_count: int

    character_count: int