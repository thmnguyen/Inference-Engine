import re
from constants import LOGIC_OPERANDS
from utils import *

def get_tokens(sequence: str):
    # Extract tokens from a sequence string.
    regex_logical = r"\w+\d+|\w+|=>|<=>|~|\)|\(|&|\|\|"
    tokens = sequence.replace(" ", "")
    tokens = re.findall(regex_logical, tokens)
    return tokens

def infix_to_postfix(sequence: str):
    # Convert an infix expression to postfix.
    stack = []
    queue = []
    tokens = get_tokens(sequence)
    
    for t in tokens:
        if t == "(":
            stack.append(t)
        elif t == ")":
            while stack and stack[-1] != "(":
                queue.append(stack.pop())
            stack.pop()  # Remove '(' from stack
        elif t in LOGIC_OPERANDS:
            if stack and stack[-1] == "~" and t == "~":
                stack.pop()
                continue
            while stack and stack[-1] != "(" and LOGIC_OPERANDS[t] <= LOGIC_OPERANDS[stack[-1]]:
                queue.append(stack.pop())
            stack.append(t)
        else:
            queue.append(t)
    
    while stack:
        queue.append(stack.pop())
    
    return queue

def infix_to_prefix(sequence):
    # Convert an infix expression to prefix.
    sequence = sequence.replace("~~", "")  # Remove double negations
    
    if len(sequence) == 1:
        return sequence

    tokens = get_tokens(sequence)[::-1]
    new_sequence = []
    
    for token in tokens:
        if token == "(":
            new_sequence.append(")")
        elif token == ")":
            new_sequence.append("(")
        else:
            new_sequence.append(token)
    
    reversed_sequence = "".join(new_sequence)
    prefix = infix_to_postfix(reversed_sequence)[::-1]
    
    return prefix

def construct_expression_tree(sequence):
    # Construct expression tree in prefix order for CNF.
    stack = []
    expression = infix_to_prefix(sequence)[::-1]
    
    if len(expression) == 1:
        return expression
    
    for token in expression:
        if token == "~":
            right = stack.pop()
            node = [token, right]
            stack.append(node)
        elif token in LOGIC_OPERANDS:
            left = stack.pop()
            right = stack.pop()
            node = [token, left, right]
            stack.append(node)
        else:
            stack.append(token)
    
    return stack[0]

def postfix_to_infix(sequence):
    # Convert postfix to infix for Truth Table and CNF.
    stack = []
    
    for token in sequence:
        if token not in LOGIC_OPERANDS:
            stack.append(token)
        else:
            if len(stack) >= 1 and token == "~":
                right = stack.pop()
                stack.append(f"(~{right})")
            elif len(stack) >= 2 and token != "~":
                right = stack.pop()
                left = stack.pop()
                if token == "=>":
                    stack.append(f"(~{left} | {right})")
                elif token == "<=>":
                    stack.append(f"(({left} & {right}) | (~{left} & ~{right}))")
                elif token == "||":
                    stack.append(f"({left} | {right})")
                else:
                    stack.append(f"({left} {token} {right})")
    
    return stack.pop()

def prefix_to_infix(expression):
    # Convert prefix to infix for CNF.
    if isinstance(expression, str):
        return expression
    
    operator = expression[0]
    
    if operator == "~":
        operand = prefix_to_infix(expression[1])
        return f"~{operand}"
    elif operator in ["||", "&"]:
        operands = [prefix_to_infix(exp) for exp in expression[1:]]
        return f"({f' {operator} '.join(operands)})"

