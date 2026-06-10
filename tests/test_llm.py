from services.llm.gemini_provider import GeminiProvider
from services.llm.llm_service import LLMService


def test_llm_service_uses_context_when_gemini_key_is_missing() -> None:
    service = LLMService(provider=GeminiProvider(api_key=""))

    answer = service.answer("What is this about?", ["The policy covers invoices."])

    assert "Gemini is not configured" in answer
    assert "policy covers invoices" in answer
