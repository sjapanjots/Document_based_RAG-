from core.config import settings
from services.chunking.chunking_strategy import ChunkingStrategy


class SlidingWindowChunker(ChunkingStrategy):
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

        step = self.chunk_size - self.overlap
        return [
            normalized[index:index + self.chunk_size].strip()
            for index in range(0, len(normalized), step)
            if normalized[index:index + self.chunk_size].strip()
        ]
