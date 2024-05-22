from CnfConverter import to_cnf_form_prefix
from KnowledgeBase import KnowledgeBase
from Algorithms.InferenceAlgorithm import InferenceAlgorithm

class DPLL(InferenceAlgorithm):
    def __init__(self, knowledge_base: KnowledgeBase):
        super().__init__(knowledge_base)
        self.name = "DPLL"

    # Method to generate a list of the complements for all symbols in the model
    def get_complements(self, model: list) -> list:
        result = []
        for symbol in model:
            if type(symbol) is str:
                result.append(["~", symbol])
            else:
                result.append(symbol[1])
        return result
    
    # Method to check if all clauses are true in the model
    def all_clauses_true(self, clauses, model):
        for clause in clauses[1:]:
            if len([var for var in clause[1:] if var in model]) == 0:
                return False
        return True

    # Method to check if any clause is false in the model
    def any_clause_false(self, clauses, model: list) -> bool:
        model_negated = self.get_complements(model)
        for clause in clauses[1:]:
            if len([var for var in clause[1:] if var not in model_negated]) == 0:
                return True
        return False
    
    # Method to find a pure literal not yet assigned a value in the model
    def find_pure_literal(self, clauses, model: list):
        model_negated = self.get_complements(model)
        candidates = []
        for clause in clauses[1:]:
            if len([symbol for symbol in clause[1:] if symbol in model]) == 0:
                candidates = candidates + [symbol for symbol in clause[1:]]
        candidates_negated = self.get_complements(candidates)
        pure = [symbol for symbol in candidates if symbol not in candidates_negated]
        for symbol in pure:
            if symbol not in model and symbol not in model_negated:
                return symbol
        return False

    # Method to find a unit clause not yet assigned a value in the model
    def find_unit_clause(self, clauses, model: list):
        model_negated = self.get_complements(model)
        for clause in clauses[1:]:
            remaining = [symbol for symbol in clause[1:] if symbol not in model_negated]
            if len(remaining) == 1:
                if remaining[0] not in model:
                    return remaining[0]
        return False

    # Method to pick a symbol not yet assigned a value in the model
    def pick_literal(self, clauses, model: list):
        combined = model + self.get_complements(model)
        for clause in clauses[1:]:
            for literal in clause[1:]:
                if type(literal) is str and literal not in combined:
                    return literal
        return False

    def dpll(self, cnf, model):
        # If all clauses are true, the current model is a satisfying assignment
        if self.all_clauses_true(cnf, model):
            return model
        # If any clause is false, the current model is not a satisfying assignment
        if self.any_clause_false(cnf, model):
            return False
        # Find a pure literal
        pure = self.find_pure_literal(cnf, model)
        if pure:
            return self.dpll(cnf, model + [pure])
        # Find a unit clause
        unit = self.find_unit_clause(cnf, model)
        if unit:
            return self.dpll(cnf, model + [unit])
        pick = self.pick_literal(cnf, model)
        if pick:
            # try positive
            result = self.dpll(cnf, model + [pick])
            if result:
                return result
            else:
                # try negative
                result = self.dpll(cnf, model + [['~', pick]])
                if result:
                    return result
                else:
                    return False
                
    def stabilize_clause(self, clause):
        if type(clause) is str: # a single positive literal
            return ["&", ["||", clause]]
        elif clause[0] == "~": # a single negative literal
            return ["&", ["||", clause]]
        elif clause[0] == "||": # a single clause
            return ["&", clause]
        else:
            result = ["&"]
            for sub_clause in clause[1:]:
                if type(sub_clause) == str:
                    result.append(["||", sub_clause])
                elif sub_clause[0] == "~":
                    result.append(["||", sub_clause])
                else:
                    result.append(sub_clause)
            return result

    def entails(self) -> tuple[bool, list]:
        query = self.knowledge_base.query[0]
        q_content = query.raw_content
        q_content = "~(" + q_content + ")"
        # Prepare the query in CNF form
        cnf_q = to_cnf_form_prefix(q_content)
        list_sentence = []
        for sentence in self.knowledge_base.sentences:
            cnf_sentence = to_cnf_form_prefix(sentence.raw_content)
            if (cnf_sentence[0] == "&"):
                cnf_sentence = cnf_sentence[1:]
                for sub_clause in cnf_sentence:
                    list_sentence.append(sub_clause)
            else:
                list_sentence.append(cnf_sentence)
        # Add the query to the list of sentences
        if (cnf_q[0] == "&"):
            cnf_q = cnf_q[1:]
            for sub_clause in cnf_q:
                list_sentence.append(sub_clause)
        else:
            list_sentence.append(cnf_q)
        list_sentence = ["&"] + list_sentence
        ans = self.dpll(self.stabilize_clause(list_sentence), [])
        return not bool(ans), []
