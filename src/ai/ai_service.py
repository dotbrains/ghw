from abc import ABC, abstractmethod

class AIService(ABC):
    @abstractmethod
    def generate_commit_message(self, diff_output: str) -> str:
        pass
