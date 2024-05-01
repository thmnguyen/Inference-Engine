from abc import ABC, abstractmethod
from KnowledgeBase import KnowledgeBase
from LogicSentence import LogicSentence

class InferenceAlgorithm(ABC):
    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base

    @abstractmethod
    def entails(self) -> tuple[bool, int]:
        pass

class TruthTableAlgorithm(InferenceAlgorithm):
    def __init__(self, knowledge_base: KnowledgeBase):
        super().__init__(knowledge_base)
        self.count = 0
        self.query = LogicSentence()

    def check_all_models(self, symbols: list, model: list[tuple[str, bool]]):
        # Recursively check all possible models and count the satisfying ones.
        if len(symbols) == 0:
            result = True
            if self.knowledge_base.is_model_valid(model):
                result = self.query.evaluate(model)
                if result:
                    self.count += 1
            return result
        else:
            p = symbols[0]
            rest = symbols[1:]
            return self.check_all_models(rest, model + [(p, True)]) and self.check_all_models(rest, model + [(p, False)])

    def entails(self) -> tuple[bool, int]:
        # Check if the knowledge base entails the query using the truth table algorithm.
        symbols = list(self.knowledge_base.symbols.keys())
        self.query = self.knowledge_base.query[0]
        result = self.check_all_models(symbols, [])
        if not result:
            self.count = 0
        return result, self.count

class ForwardChainingAlgorithm(InferenceAlgorithm):
    def __init__(self, knowledge_base: KnowledgeBase):
        super().__init__(knowledge_base)
        self.count = 0
        self.query = LogicSentence()
        self.truth_table = []

class BackwardChainingAlgorithm(InferenceAlgorithm):
    def __init__(self, knowledge_base: KnowledgeBase):
        super().__init__(knowledge_base)
        self.count = 0
        self.query = LogicSentence()