from pathlib import Path

from core.logger import get_logger
from services.pdf.pymupdf import (
    PyMuPDFReader
)

logger = get_logger(__name__)


class PDFService:

    def __init__(self):
        self.reader = PyMuPDFReader()

    def process_document(
        self,
        file_path: str
    ) -> dict:

        logger.info(
            "Processing document: %s",
            file_path
        )

        text = self.reader.extract_text(
            file_path
        )

        metadata = (
            self.reader.extract_metadata(
                file_path
            )
        )

        return {
            "filename": Path(file_path).name,
            "text": text,
            "page_count": metadata[
                "page_count"
            ],
            "character_count": len(text)
        }
        