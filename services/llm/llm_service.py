from core.config import settings
from services.llm.gemini_provider import GeminiProvider
from services.llm.llm_provider import LLMProvider


class LLMService:
    def __init__(self, provider: LLMProvider | None = None) -> None:
        self.provider = provider or GeminiProvider()

    def answer(
        self,
        question: str,
        contexts: list[str],
        gemini_api_key: str | None = None,
        gemini_model: str | None = None,
    ) -> str:
        prompt = self._build_prompt(question, contexts)
        if gemini_api_key or gemini_model:
            provider = GeminiProvider(
                api_key=gemini_api_key or "",
                model_name=gemini_model or settings.GEMINI_MODEL,
            )
            return provider.generate(prompt)

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
