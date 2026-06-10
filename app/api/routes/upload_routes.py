from pathlib import Path

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    UploadFile
)

from core.config import settings
from app.schemas.response import UploadResponse
from services.pdf.pdfservice import PDFService
from utils.file_handler import FileHandler
from utils.validator import FileValidator


router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

pdf_service = PDFService()


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
        file_path.write_bytes(contents)

    except Exception as exception:

        raise HTTPException(
            status_code=500,
            detail=f"Failed to save file: {exception}"
        )

    # -----------------------------
    # Process PDF
    # -----------------------------

    try:
        document_info = (
            pdf_service.process_document(
                str(file_path)
            )
        )
    except ValueError as exception:
        raise HTTPException(
            status_code=400,
            detail=str(exception),
        ) from exception
    except Exception as exception:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process PDF: {exception}",
        ) from exception

    return UploadResponse(
        filename=document_info["filename"],
        page_count=document_info["page_count"],
        character_count=document_info["character_count"],
        chunk_count=document_info["chunk_count"],
    )
