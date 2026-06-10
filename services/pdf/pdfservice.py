from pathlib import Path

from core.logger import get_logger
from services.chunking.chunk_service import ChunkService
from services.embeddings.embedding_service import EmbeddingService
from services.embeddings.sentence_transformer import SentenceTransformerEmbeddingService
from services.pdf.pymupdf import (
    PyMuPDFReader
)
from services.vectorstore.faiss_store import FAISSVectorStore
from services.vectorstore.vector_store import VectorStore

logger = get_logger(__name__)


class PDFService:

    def __init__(
        self,
        reader: PyMuPDFReader | None = None,
        chunk_service: ChunkService | None = None,
        embedding_service: EmbeddingService | None = None,
        vector_store: VectorStore | None = None,
    ) -> None:
        self.reader = reader or PyMuPDFReader()
        self.chunk_service = chunk_service or ChunkService()
        self.embedding_service = embedding_service or SentenceTransformerEmbeddingService()
        self.vector_store = vector_store or FAISSVectorStore()

    def process_document(
        self,
        file_path: str
    ) -> dict:

        logger.info(
            "Processing document: %s",
            file_path
        )

        text = self.reader.extract_text(file_path)
        if not text.strip():
            raise ValueError("PDF does not contain extractable text.")

        metadata = (
            self.reader.extract_metadata(
                file_path
            )
        )
        chunks = self.chunk_service.create_chunks(text)
        vectors = self.embedding_service.embed_documents(chunks)
        filename = Path(file_path).name
        metadatas = [
            {
                "filename": filename,
                "chunk_index": index,
                "page_count": metadata["page_count"],
            }
            for index, _ in enumerate(chunks)
        ]
        self.vector_store.add(vectors, chunks, metadatas)

        return {
            "filename": filename,
            "text": text,
            "page_count": metadata[
                "page_count"
            ],
            "character_count": len(text),
            "chunk_count": len(chunks),
        }
        
