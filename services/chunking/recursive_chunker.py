from core.config import settings
from services.chunking.chunking_strategy import ChunkingStrategy


class RecursiveChunker(ChunkingStrategy):
    def __init__(
        self,
        chunk_size: int = settings.CHUNK_SIZE,
        overlap: int = settings.CHUNK_OVERLAP,
    ) -> None:
        if overlap >= chunk_size:
            raise ValueError("overlap must be smaller than chunk_size")
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> list[str]:
        normalized = " ".join(text.split())
        if not normalized:
            return []

        chunks: list[str] = []
        start = 0

        while start < len(normalized):
            end = min(start + self.chunk_size, len(normalized))
            split_at = self._best_split(normalized, start, end)
            chunk = normalized[start:split_at].strip()
            if chunk:
                chunks.append(chunk)

            if split_at >= len(normalized):
                break
            start = max(split_at - self.overlap, start + 1)

        return chunks

    @staticmethod
    def _best_split(text: str, start: int, end: int) -> int:
        if end >= len(text):
            return len(text)

        window = text[start:end]
        for separator in (". ", "? ", "! ", "\n", " "):
            index = window.rfind(separator)
            if index > max(0, len(window) // 2):
                return start + index + len(separator)

        return end
