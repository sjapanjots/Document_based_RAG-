from services.chat.chat_service import ChatService
from services.embeddings.sentence_transformer import SentenceTransformerEmbeddingService
from services.llm.llm_service import LLMService
from services.pdf.pdfservice import PDFService
from services.retrieval.retrieval_service import RetrievalService
from services.vectorstore.faiss_store import FAISSVectorStore


class ServiceContainer:
    def __init__(self) -> None:
        self.vector_store = FAISSVectorStore()
        self.embedding_service = SentenceTransformerEmbeddingService()
        self.pdf_service = PDFService(
            embedding_service=self.embedding_service,
            vector_store=self.vector_store,
        )
        self.retrieval_service = RetrievalService(
            embedding_service=self.embedding_service,
            vector_store=self.vector_store,
        )
        self.llm_service = LLMService()
        self.chat_service = ChatService(
            retrieval_service=self.retrieval_service,
            llm_service=self.llm_service,
        )


container = ServiceContainer()
