from pathlib import Path

from core.logger import get_logger

logger = get_logger(__name__)


class FileHandler:

    @staticmethod
    def create_directory(path: str) -> None:
        Path(path).mkdir(
            parents=True,
            exist_ok=True
        )

        logger.info(
            "Directory ensured: %s",
            path
        )