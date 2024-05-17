from CnfConverter import to_cnf_form_prefix
from KnowledgeBase import KnowledgeBase
from Algorithms.InferenceAlgorithm import InferenceAlgorithm

class DPLL(InferenceAlgorithm):
    def __init__(self, knowledge_base: KnowledgeBase):
        super().__init__(knowledge_base)
        self.name = "DPLL"

    def negate_literal(self, literal):
        if isinstance(literal, str):
            return ["~", literal]
        else:
            return literal[1]

    def is_clause_satisfied(self, clause, model):
        for literal in clause[1:]:
            if literal in model:
                return True
        return False

    def is_clause_unsatisfied(self, clause, model):
        for literal in clause[1:]:
            if self.negate_literal(literal) not in model:
                return False
        return True

    def find_pure_literal(self, clauses, model):
        literals = set()
        negated_literals = set()
        
        def convert_to_tuple(literal):
            if isinstance(literal, list):
                return tuple(convert_to_tuple(item) for item in literal)
            else:
                return literal
        
        for clause in clauses[1:]:
            for literal in clause[1:]:
                if isinstance(literal, str):
                    literals.add(literal)
                else:
                    negated_literals.add(convert_to_tuple(literal))  # Recursively convert nested lists to tuples
        
        pure_literals = literals - {literal[1] for literal in negated_literals}  # Convert negated literals to a set of strings
        for literal in pure_literals:
            if literal not in model and self.negate_literal(literal) not in model:
                return literal
        return None

    def find_unit_clause(self, clauses, model):
        for clause in clauses[1:]:
            unassigned_literals = [literal for literal in clause[1:] if literal not in model and self.negate_literal(literal) not in model]
            if len(unassigned_literals) == 1:
                return unassigned_literals[0]
        return None

    def pick_unassigned_literal(self, clauses, model):
        for clause in clauses[1:]:
            for literal in clause[1:]:
                if literal not in model and self.negate_literal(literal) not in model:
                    return literal
        return None

    def dpll(self, clauses, model):
        if all(self.is_clause_satisfied(clause, model) for clause in clauses[1:]):
            return model
        if any(self.is_clause_unsatisfied(clause, model) for clause in clauses[1:]):
            return None

        literal = self.find_pure_literal(clauses, model)
        if literal is not None:
            return self.dpll(clauses, model + [literal])

        literal = self.find_unit_clause(clauses, model)
        if literal is not None:
            return self.dpll(clauses, model + [literal])

        literal = self.pick_unassigned_literal(clauses, model)
        if literal is not None:
            result = self.dpll(clauses, model + [literal])
            if result is not None:
                return result
            return self.dpll(clauses, model + [self.negate_literal(literal)])

        return None

    def entails(self) -> tuple[bool, list]:
        if not self.knowledge_base.query:
            return False, []  # Return False if the query list is empty

        query = self.knowledge_base.query[0]
        q_content = "~(" + query.raw_content + ")"
        cnf_q = to_cnf_form_prefix(q_content)

        clauses = ["&"]
        for sentence in self.knowledge_base.sentences:
            cnf_sentence = to_cnf_form_prefix(sentence.raw_content)
            if cnf_sentence[0] == "&":
                clauses.extend(cnf_sentence[1:])
            else:
                clauses.append(cnf_sentence)

        if cnf_q[0] == "&":
            clauses.extend(cnf_q[1:])
        else:
            clauses.append(cnf_q)

        result = self.dpll(clauses, [])
        return result is None, []
    