from pathlib import Path

from core.constant import ALLOWED_EXTENSIONS


class FileValidator:

    @staticmethod
    def validate_extension(filename: str) -> bool:
        extension = Path(filename).suffix.lower()

        return extension in ALLOWED_EXTENSIONS