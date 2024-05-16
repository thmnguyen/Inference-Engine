from abc import ABC, abstractmethod
class InferenceAlgorithm(ABC):
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base
    @abstractmethod
    def entails(self) -> tuple[bool, int]:
        pass


