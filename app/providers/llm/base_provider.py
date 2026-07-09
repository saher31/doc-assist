from abc import ABC, abstractmethod


class BaseLLmProvider(ABC):
    @abstractmethod
    def generate(self, context: str, question: str):
        pass