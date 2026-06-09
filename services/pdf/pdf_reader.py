from abc import ABC, abstractmethod


class PDFReader(ABC):

    @abstractmethod
    def extract_text(self, file_path: str) -> str:
        pass

    @abstractmethod
    def extract_metadata(self, file_path: str) -> dict:
        pass