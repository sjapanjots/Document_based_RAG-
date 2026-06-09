from pathlib import Path

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile
)

from core.config import settings
from schemas.reponse import UploadResponse
from services.pdf.pdf_reader import PDFReader
from utils.file_handler import FileHandler
from utils.validator import FileValidator


router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

pdf_service = PDFReader()


@router.post(
    "/",
    response_model=UploadResponse
)
async def upload_document(
    file: UploadFile = File(...)
) -> UploadResponse:

    # -----------------------------
    # Validate filename
    # -----------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing."
        )

    filename = file.filename

    # -----------------------------
    # Validate extension
    # -----------------------------

    if not FileValidator.validate_extension(
        filename
    ):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # -----------------------------
    # Ensure upload directory exists
    # -----------------------------

    FileHandler.create_directory(
        settings.UPLOAD_DIRECTORY
    )

    # -----------------------------
    # Save file
    # -----------------------------

    file_path = (
        Path(settings.UPLOAD_DIRECTORY)
        / filename
    )

    try:

        contents = await file.read()

        with open(
            file_path,
            "wb"
        ) as buffer:
            buffer.write(contents)

    except Exception as exception:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {exception}"
        )

    # -----------------------------
    # Process PDF
    # -----------------------------

    document_info = (
        pdf_service.process_document(
            str(file_path)
        )
    )

    return UploadResponse(
        filename=document_info["filename"],
        page_count=document_info["page_count"],
        character_count=document_info["character_count"]
    )