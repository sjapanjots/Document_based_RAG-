import pickle
from pathlib import Path
from typing import Any

import numpy as np

from core.config import settings
from core.logger import get_logger
from services.vectorstore.vector_store import VectorStore


logger = get_logger(__name__)


class FAISSVectorStore(VectorStore):
    def __init__(self, storage_dir: str = settings.VECTOR_DB_DIRECTORY) -> None:
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.index_path = self.storage_dir / "index.faiss"
        self.metadata_path = self.storage_dir / "chunks.pkl"
        self.dimension = settings.EMBEDDING_DIMENSION
        self.texts: list[str] = []
        self.metadatas: list[dict[str, Any]] = []
        self._vectors = np.empty((0, self.dimension), dtype="float32")
        self._faiss = self._load_faiss()
        self._index = None
        self._load()

    def add(
        self,
        vectors: list[list[float]],
        texts: list[str],
        metadatas: list[dict[str, Any]],
    ) -> None:
        if not vectors:
            return

        matrix = np.asarray(vectors, dtype="float32")
        incoming_dimension = matrix.shape[1]
        if len(self._vectors) == 0:
            self.dimension = incoming_dimension
            self._vectors = np.empty((0, self.dimension), dtype="float32")
        elif incoming_dimension != self.dimension:
            raise ValueError(
                f"Vector dimension mismatch: expected {self.dimension}, "
                f"received {incoming_dimension}"
            )

        self.texts.extend(texts)
        self.metadatas.extend(metadatas)
        self._vectors = np.vstack([self._vectors, matrix])

        if self._faiss is not None:
            if self._index is None or self._index.d != self.dimension:
                self._index = self._faiss.IndexFlatIP(self.dimension)
                if len(self._vectors):
                    self._index.add(self._vectors)
            else:
                self._index.add(matrix)

        self._save()

    def search(self, query_vector: list[float], top_k: int) -> list[dict[str, Any]]:
        if not self.texts:
            return []

        query = np.asarray([query_vector], dtype="float32")

        if self._faiss is not None and self._index is not None:
            scores, indices = self._index.search(query, min(top_k, len(self.texts)))
            pairs = zip(indices[0].tolist(), scores[0].tolist())
        else:
            scores = (self._vectors @ query[0]).tolist()
            ranked = sorted(enumerate(scores), key=lambda item: item[1], reverse=True)
            pairs = ranked[:top_k]

        results: list[dict[str, Any]] = []
        for index, score in pairs:
            if index < 0:
                continue
            results.append(
                {
                    "text": self.texts[index],
                    "score": float(score),
                    "metadata": self.metadatas[index],
                }
            )
        return results

    @staticmethod
    def _load_faiss():
        try:
            import faiss

            return faiss
        except Exception as exception:
            logger.warning("FAISS unavailable, using NumPy vector search: %s", exception)
            return None

    def _load(self) -> None:
        if self.metadata_path.exists():
            with self.metadata_path.open("rb") as file:
                payload = pickle.load(file)
            self.texts = payload.get("texts", [])
            self.metadatas = payload.get("metadatas", [])
            self._vectors = payload.get("vectors", self._vectors)

        if self._faiss is not None and self.index_path.exists():
            self._index = self._faiss.read_index(str(self.index_path))
        elif self._faiss is not None and len(self._vectors):
            self._index = self._faiss.IndexFlatIP(self._vectors.shape[1])
            self._index.add(self._vectors)

    def _save(self) -> None:
        with self.metadata_path.open("wb") as file:
            pickle.dump(
                {
                    "texts": self.texts,
                    "metadatas": self.metadatas,
                    "vectors": self._vectors,
                },
                file,
            )

        if self._faiss is not None and self._index is not None:
            self._faiss.write_index(self._index, str(self.index_path))
