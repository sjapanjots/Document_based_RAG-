from typing import Any

from core.config import settings
from services.llm.llm_service import LLMService
from services.retrieval.retrieval_service import RetrievalService


class ChatService:
    def __init__(
        self,
        retrieval_service: RetrievalService | None = None,
        llm_service: LLMService | None = None,
    ) -> None:
        self.retrieval_service = retrieval_service or RetrievalService()
        self.llm_service = llm_service or LLMService()

    def ask(self, question: str, top_k: int | None = None) -> dict[str, Any]:
        sources = self.retrieval_service.retrieve(question, top_k or settings.TOP_K)
        answer = self.llm_service.answer(
            question,
            [source["text"] for source in sources],
        )
        return {
            "answer": answer,
            "sources": sources,
        }
