from abc import ABC, abstractmethod
from KnowledgeBase import KnowledgeBase
from LogicSentence import LogicSentence
from Algorithms.InferenceAlgorithm import*
class BackwardChainingAlgorithm(InferenceAlgorithm):
    def __init__(self, knowledge_base: KnowledgeBase):
        super().__init__(knowledge_base)
        self.name = "BC"
        self.count = 0
        self.query = LogicSentence()
        self.fact = dict()
        self.output = []
        
    def check_all(self, visited: list, goal):
        # Check if goal is in fact then add to output
        if goal in self.fact.keys() and self.fact[goal]:
            if goal not in self.output:
                self.output.append(goal)
            return True

        for sentence in self.knowledge_base.sentences:
            # Check if goal is in conclusion of sentence
            if sentence.conclusion == goal:
                symbolCount = 0
                for premise in sentence.premises:
                    # Check if premise is also the goal then break to avoid infinite loop
                    if premise == goal:
                        break
                    # Check if premise is visited then break to avoid infinite loop
                    if premise in visited:
                        if self.fact[premise] == False: 
                            break
                    else:
                        visited.append(premise)
                    # Update fact of premise
                    self.fact[premise] = self.check_all(visited.copy(), premise)
                    # Check if premise is false then break to avoid infinite loop
                    if (self.fact[premise] == False):
                        break
                    symbolCount += 1
                # Check if all premises are satisfied then add to output
                if symbolCount == len(sentence.premises):
                    if goal not in self.output:
                        self.output.append(goal)
                    return True
        return False

    def entails(self) -> tuple[bool, list]:
        # Initialize fact
        self.query = self.knowledge_base.query[0]
        for symbol in self.knowledge_base.symbols:
            # Initialize fact of symbol to False
            self.fact[symbol] = False

        for sentence in self.knowledge_base.sentences:
            
            if len(sentence.content) == 1:
                # Initialize fact of standalone symbol to True
                self.fact[sentence.content[0]] = True
                
        # Run backward chaining
        ans = self.check_all([], self.query.conclusion)
        if ans:
            return (ans, self.output)
        else:
            return (ans, [])