from abc import ABC, abstractmethod
from KnowledgeBase import KnowledgeBase
from LogicSentence import LogicSentence
from Algorithms.InferenceAlgorithm import*
class BackwardChainingAlgorithm(InferenceAlgorithm):
    def __init__(self, knowledge_base: KnowledgeBase):
        super().__init__(knowledge_base)
        self.count = 0
        self.query = LogicSentence()