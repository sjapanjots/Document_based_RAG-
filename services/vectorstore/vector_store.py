from abc import ABC, abstractmethod
from typing import Any


class VectorStore(ABC):
    @abstractmethod
    def add(
        self,
        vectors: list[list[float]],
        texts: list[str],
        metadatas: list[dict[str, Any]],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def search(self, query_vector: list[float], top_k: int) -> list[dict[str, Any]]:
        raise NotImplementedError
