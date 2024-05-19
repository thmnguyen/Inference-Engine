import random
from constants import LOGIC_OPERANDS

PROBABILITY_OF_HORN_QUERY_BEING_AN_EXPRESSION = 0.7
PROBABILITY_OF_QUERY_BEING_AN_EXPRESSION = 0.6

def generate_horn_clause(num_symbols, number_of_horn_clauses=10):
    symbols = set(random.sample([chr(i) for i in range(ord("a"), ord("z") + 1)], num_symbols))
    horn_clauses, single_literals = set(), set()
    while len(horn_clauses) + len(single_literals) < number_of_horn_clauses:
        consequent = random.choice(list(symbols))
        if random.random() <= PROBABILITY_OF_HORN_QUERY_BEING_AN_EXPRESSION:
            antecedents = random.sample(symbols - {consequent}, random.randint(1, num_symbols - 1))
            horn_clauses.add(f"{' & '.join(antecedents)} => {consequent}")
        else:
            single_literals.add(consequent)
    tell = "; ".join(horn_clauses) + (";" if horn_clauses else "") + (" " + "; ".join(single_literals) + ";" if single_literals else "")
    return f"TELL\n{tell}\nASK\n{random.choice(list(symbols))}\n"

def generate_random_expression(propositions, depth):
    if depth == 0 or len(propositions) == 1:
        return random.choice(propositions)
    else:
        operator = random.choices(list(LOGIC_OPERANDS.keys()), weights=list(LOGIC_OPERANDS.values()))[0]
        if operator == "~":
            operand = generate_random_expression(propositions, depth - 1)
            return f"~{operand}"
        else:
            num_operands = random.randint(2, len(propositions))
            operands = random.sample(propositions, num_operands)
            subexpressions = [generate_random_expression([p for p in propositions if p != op], depth - 1) for op in operands]
            while any(f"~{op}" in subexpressions for op in operands):
                subexpressions = [generate_random_expression([p for p in propositions if p != op], depth - 1) for op in operands]
            expression = f" {operator} ".join(subexpressions)
            return f"({expression})"

def generate_random_tests(num_propositions, num_expression, depth):
    propositions = random.sample([chr(i) for i in range(ord("a"), ord("z") + 1)], num_propositions)
    knowledge_base = "; ".join(set(generate_random_expression(propositions, depth) for _ in range(num_expression)))
    query = generate_random_expression(propositions, depth) if random.random() < PROBABILITY_OF_QUERY_BEING_AN_EXPRESSION else random.choice(propositions)
    return f"TELL\n{knowledge_base}\nASK\n{query}"
