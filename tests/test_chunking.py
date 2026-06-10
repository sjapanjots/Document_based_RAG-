from services.chunking.recursive_chunker import RecursiveChunker
from services.chunking.sliding_chunker import SlidingWindowChunker


def test_recursive_chunker_returns_overlapping_chunks() -> None:
    text = " ".join(f"word{i}" for i in range(80))
    chunker = RecursiveChunker(chunk_size=80, overlap=10)

    chunks = chunker.chunk(text)

    assert len(chunks) > 1
    assert all(len(chunk) <= 80 for chunk in chunks)


def test_sliding_window_chunker_handles_empty_text() -> None:
    chunker = SlidingWindowChunker(chunk_size=50, overlap=10)

    assert chunker.chunk("   ") == []
