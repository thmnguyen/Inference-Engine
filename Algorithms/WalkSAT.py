import random
from abc import ABC
from KnowledgeBase import KnowledgeBase
from Algorithms.InferenceAlgorithm import*
from CnfConverter import to_cnf_form_prefix

class WalkSAT(InferenceAlgorithm):
    def __init__(self, knowledge_base: KnowledgeBase):
        super().__init__(knowledge_base)
        #self.name = "WalkSAT"

    def random_assignment(self, cnf_formula):
        symbols = set()
        for clause in cnf_formula[1:]:
            for literal in clause[1:]:
                if isinstance(literal, list):
                    if len(literal) > 1 and isinstance(literal[1], str):
                        symbol = literal[1]
                        symbols.add(symbol)
                elif isinstance(literal, str):
                    symbols.add(literal)
        return {symbol: random.choice([True, False]) for symbol in symbols}

    def is_satisfied(self, cnf_formula, model):
        for clause in cnf_formula[1:]:
            if not self.is_clause_satisfied(clause, model):
                return False
        return True

    def is_clause_satisfied(self, clause, model):
        for literal in clause[1:]:
            if isinstance(literal, list):
                if len(literal) > 1:
                    symbol = literal[1]
                    if isinstance(symbol, list):
                        return False  # Skip clauses with nested lists
                    if not model[symbol]:
                        return True
            else:
                if model[literal]:
                    return True
        return False

    def choose_unsatisfied_clause(self, cnf_formula, model):
        unsatisfied_clauses = [clause for clause in cnf_formula[1:] if not self.is_clause_satisfied(clause, model)]
        return random.choice(unsatisfied_clauses)

    def random_symbol(self, clause):
        literals = [literal[1] if isinstance(literal, list) else literal for literal in clause[1:]]
        if not literals:
            return None  # Return None if the clause is empty or contains only the operator
        return random.choice(literals)

    def max_score_symbol(self, cnf_formula, clause, model):
        scores = {}
        for literal in clause[1:]:
            if isinstance(literal, list) and len(literal) > 1:
                symbol = literal[1]
                if isinstance(symbol, list):
                    continue  # Skip literals with nested lists
            else:
                symbol = literal
            
            if isinstance(symbol, list):
                continue  # Skip symbols that are lists
            
            model[symbol] = not model[symbol]
            score = sum(1 for clause in cnf_formula[1:] if self.is_clause_satisfied(clause, model))
            scores[symbol] = score
            model[symbol] = not model[symbol]  # Revert the change
        
        if not scores:
            return None  # Return None if no valid symbols are found
        
        return max(scores, key=scores.get)

    def entails(self) -> tuple[bool, list]:
        if not self.knowledge_base.query:
            return False, []  # Return False if the query list is empty

        query = self.knowledge_base.query[0]
        q_content = query.raw_content

        # Prepare the knowledge base sentences in CNF form
        cnf_kb = ["&"]
        for sentence in self.knowledge_base.sentences:
            cnf_sentence = to_cnf_form_prefix(sentence.raw_content)
            cnf_kb.append(cnf_sentence)

        # Prepare the negated query in CNF form
        cnf_q = to_cnf_form_prefix(f"~({q_content})")

        # Run the WalkSAT algorithm on the knowledge base
        max_flips = 1000  # Maximum number of flips
        max_tries = 10    # Maximum number of tries
        p = 0.5           # Probability of random walk

        for _ in range(max_tries):
            model = self.random_assignment(cnf_kb)
            for _ in range(max_flips):
                if self.is_satisfied(cnf_kb, model):
                    # Knowledge base is satisfiable, check if the query is entailed
                    if not self.is_satisfied(["&", cnf_q], model):
                        return True, model  # Query is entailed, return the satisfying model
                    else:
                        break  # Query is not entailed, try again
                clause = self.choose_unsatisfied_clause(cnf_kb, model)
                if random.random() < p:
                    symbol = self.random_symbol(clause)
                    if symbol is None or isinstance(symbol, list):
                        continue  # Skip the current iteration if no valid symbol is chosen
                else:
                    symbol = self.max_score_symbol(cnf_kb, clause, model)
                    if symbol is None or isinstance(symbol, list):
                        continue  # Skip the current iteration if no valid symbol is chosen
                model[symbol] = not model[symbol]
        return False, []  # Knowledge base is unsatisfiable or query is not entailed