from services.chunking.chunking_strategy import ChunkingStrategy
from services.chunking.recursive_chunker import RecursiveChunker


class ChunkService:
    def __init__(self, strategy: ChunkingStrategy | None = None) -> None:
        self.strategy = strategy or RecursiveChunker()

    def create_chunks(self, text: str) -> list[str]:
        return self.strategy.chunk(text)
