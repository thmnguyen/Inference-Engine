from abc import ABC, abstractmethod
from KnowledgeBase import KnowledgeBase
from LogicSentence import*
from Algorithms.InferenceAlgorithm import*
class ForwardChainingAlgorithm(InferenceAlgorithm):
    def __init__(self, knowledge_base: KnowledgeBase):
        super().__init__(knowledge_base)
        self.name = "FC"
        self.count = dict() # Count of premises for each sentence
        self.inferred = dict() # Symbols inferred to be True
        self.agenda = list()  # Symbols yet to be processed
        self.path = list() # Path of inferences leading to a conclusion
        self.query = LogicSentence()

    def check_all(self):
        query = self.query.content[0]
        print(query)
        # Process symbols in the agenda as long as it's not empty
        while len(self.agenda) > 0:
            symbol = self.agenda.pop(0) # Take the first symbol from the agenda
            if (symbol not in self.path):
                self.path.append(symbol)
            if not self.inferred[symbol]:
                self.inferred[symbol] = True
                # Decrease premise count for sentences where symbol is a premise
                for sentence in self.count:
                    if symbol in sentence.premises:
                        self.count[sentence] -= 1
                        # If all premises are inferred, add conclusion to agenda
                        if self.count[sentence] == 0:
                            if sentence.conclusion == query:
                                if (sentence.conclusion not in self.path):
                                    self.path.append(sentence.conclusion)
                                return (True, self.path)
                            self.agenda.append(sentence.conclusion)
        return False, []

    def entails(self) -> tuple[bool, list]:
        # Set query from first query in the knowledge base
        self.query = self.knowledge_base.query[0]
        q = self.query.content[0]
        # For each sentence in the knowledge base
        for sentence in self.knowledge_base.sentences:
            # If the sentence is a fact, add its conclusion to the agenda
            if len(sentence.content) == 1 and sentence.conclusion == q:
                return (True, q)
            # If the sentence is a rule, add its conclusion to the agenda
            if len(sentence.premises) > 0:
                self.count[sentence] = len(sentence.premises)
            else:
                self.agenda.append(sentence.conclusion)
        for symbol in self.knowledge_base.symbols:
            self.inferred[symbol] = False
        return self.check_all()
