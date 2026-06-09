import fitz

from services.pdf.pdf_reader import PDFReader


class PyMuPDFReader(PDFReader):

    def extract_text(self, file_path: str) -> str:
        document = fitz.open(file_path)

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        return text

    def extract_metadata(
        self,
        file_path: str
    ) -> dict:

        document = fitz.open(file_path)

        metadata = document.metadata

        page_count = document.page_count

        document.close()

        return {
            "page_count": page_count,
            "metadata": metadata
        }