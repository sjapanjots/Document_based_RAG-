from typing import Any, cast

import pymupdf

from services.pdf.pdf_reader import PDFReader


class PyMuPDFReader(PDFReader):

    def extract_text(self, file_path: str) -> str:
        document = pymupdf.open(file_path)

        pages: list[str] = []

        try:
            for page in document:
                typed_page = cast(Any, page)
                pages.append(typed_page.get_text("text"))
        finally:
            document.close()

        return "\n".join(pages)

    def extract_metadata(
        self,
        file_path: str
    ) -> dict[str, Any]:

        document = pymupdf.open(file_path)
        try:
            metadata = document.metadata
            page_count = document.page_count
        finally:
            document.close()

        return {
            "page_count": page_count,
            "metadata": metadata
        }
