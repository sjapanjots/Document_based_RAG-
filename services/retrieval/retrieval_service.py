from typing import Any

from core.config import settings
from services.embeddings.embedding_service import EmbeddingService
from services.embeddings.sentence_transformer import SentenceTransformerEmbeddingService
from services.retrieval.retriever import Retriever
from services.vectorstore.faiss_store import FAISSVectorStore
from services.vectorstore.vector_store import VectorStore


class RetrievalService(Retriever):
    def __init__(
        self,
        embedding_service: EmbeddingService | None = None,
        vector_store: VectorStore | None = None,
    ) -> None:
        self.embedding_service = embedding_service or SentenceTransformerEmbeddingService()
        self.vector_store = vector_store or FAISSVectorStore()

    def retrieve(
        self,
        question: str,
        top_k: int = settings.TOP_K,
    ) -> list[dict[str, Any]]:
        query_vector = self.embedding_service.embed_text(question)
        return self.vector_store.search(query_vector, top_k)
