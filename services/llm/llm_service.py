from services.llm.gemini_provider import GeminiProvider
from services.llm.llm_provider import LLMProvider


class LLMService:
    def __init__(self, provider: LLMProvider | None = None) -> None:
        self.provider = provider or GeminiProvider()

    def answer(self, question: str, contexts: list[str]) -> str:
        prompt = self._build_prompt(question, contexts)
        return self.provider.generate(prompt)

    @staticmethod
    def _build_prompt(question: str, contexts: list[str]) -> str:
        context = "\n\n---\n\n".join(contexts)
        return (
            "You are an enterprise document intelligence assistant. "
            "Answer only from the supplied context. If the context is insufficient, "
            "say that clearly.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n\n"
            "Answer:"
        )
