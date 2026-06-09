from pathlib import Path


class FileHandler:

    @staticmethod
    def create_directory(
        path: str
    ) -> None:

        Path(path).mkdir(
            parents=True,
            exist_ok=True
        )