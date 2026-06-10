import hashlib
import math

from core.config import settings
from core.logger import get_logger
from services.embeddings.embedding_service import EmbeddingService


logger = get_logger(__name__)


class SentenceTransformerEmbeddingService(EmbeddingService):
    def __init__(self, model_name: str = settings.EMBEDDING_MODEL_NAME) -> None:
        self.model_name = model_name
        self._model = None

    def embed_text(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        model = self._load_model()
        if model is not None:
            vectors = model.encode(texts, normalize_embeddings=True)
            return [vector.astype(float).tolist() for vector in vectors]

        return [self._hash_embedding(text) for text in texts]

    def _load_model(self):
        if self._model is not None:
            return self._model

        try:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_name)
            return self._model
        except Exception as exception:
            logger.warning(
                "SentenceTransformer unavailable, using deterministic fallback: %s",
                exception,
            )
            return None

    @staticmethod
    def _hash_embedding(text: str) -> list[float]:
        dimension = settings.EMBEDDING_DIMENSION
        vector = [0.0] * dimension
        tokens = text.lower().split()

        for token in tokens:
            digest = hashlib.sha256(token.encode("utf-8")).digest()
            index = int.from_bytes(digest[:4], "big") % dimension
            sign = 1.0 if digest[4] % 2 == 0 else -1.0
            vector[index] += sign

        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]
