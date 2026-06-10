from core.config import settings
from core.logger import get_logger
from services.llm.llm_provider import LLMProvider


logger = get_logger(__name__)


class GeminiProvider(LLMProvider):
    def __init__(
        self,
        api_key: str = settings.GEMINI_API_KEY,
        model_name: str = settings.GEMINI_MODEL,
    ) -> None:
        self.api_key = api_key
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        if not self.api_key:
            return self._fallback_answer(prompt)

        try:
            import google.generativeai as genai

            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model_name)
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as exception:
            logger.warning("Gemini generation failed, using fallback: %s", exception)
            return self._fallback_answer(prompt)

    @staticmethod
    def _fallback_answer(prompt: str) -> str:
        marker = "Context:"
        context = prompt.split(marker, 1)[-1].strip() if marker in prompt else prompt
        context = context.split("Question:", 1)[0].strip()
        if not context:
            return "I do not have enough indexed document context to answer that yet."
        return (
            "Gemini is not configured, so here is the most relevant indexed context:\n\n"
            f"{context[:1200]}"
        )
