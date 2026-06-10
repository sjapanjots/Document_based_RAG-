from abc import ABC, abstractmethod
from typing import Any


class Retriever(ABC):
    @abstractmethod
    def retrieve(self, question: str, top_k: int) -> list[dict[str, Any]]:
        raise NotImplementedError
