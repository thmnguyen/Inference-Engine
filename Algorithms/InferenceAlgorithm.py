from abc import ABC, abstractmethod
from KnowledgeBase import KnowledgeBase
class InferenceAlgorithm(ABC):
    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base

    @abstractmethod
    def entails(self) -> tuple[bool, int]:
        pass


