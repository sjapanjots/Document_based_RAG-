from pathlib import Path


class FileValidator:

    @staticmethod
    def validate_extension(
        filename: str
    ) -> bool:

        extension = (
            Path(filename)
            .suffix
            .lower()
        )

        return extension == ".pdf"