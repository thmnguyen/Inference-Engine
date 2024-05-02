import re
from constants import LOGIC_OPERANDS
from utils import*
def get_tokens(sentences: str):
    # Extract tokens from a sentence string.
    regex_logical = r"\w+\d+|\w+|=>|<=>|~|\)|\(|&|\|\|"
    tokens = sentences.replace(" ", "")
    tokens = re.findall(regex_logical, tokens)
    return tokens

def infix_to_postfix(sentences: str):
    # Convert an infix expression to postfix.
    stack = []
    queue = []
    tokens = get_tokens(sentences)
    for t in tokens:
        if t == "(":
            stack.append(t)
        elif t == ")":
            while stack[-1] != "(":
                queue.append(stack.pop())
            stack.pop()
        elif t in LOGIC_OPERANDS:
            if stack.__len__() > 0 and stack[-1] == "~" and t == "~":
                stack.pop()
                continue
            while len(stack) != 0 and stack[-1] != "(" and LOGIC_OPERANDS[t] <= LOGIC_OPERANDS[stack[-1]]:
                queue.append(stack.pop())
            stack.append(t)
        else:
            queue.append(t)
    while len(stack) != 0:
        queue.append(stack.pop())
    return queue

def execute_logic_operation(operator: str, operand1: bool, operand2: bool):
    # Execute a logic operation based on the operator and operands.
    if operator == "~":
        return not operand1
    elif operator == "||":
        return operand1 or operand2
    elif operator == "&":
        return operand1 and operand2
    elif operator == "=>":
        return not operand1 or operand2
    elif operator == "<=>":
        return operand1 == operand2