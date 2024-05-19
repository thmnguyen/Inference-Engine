from utils import*
from constants import LOGIC_OPERANDS

class LogicSentence:
    def __init__(self, raw_content: str = "", content: list = [], symbols: dict = dict()):
        self.raw_content = raw_content
        self.content = content
        self.symbols = symbols
        self.premises = []

    def set_premises(self): 
            new_content = get_tokens(self.raw_content)
            if len(new_content) == 0:
                self.conclusion = ""
            elif len(new_content) == 1:
                self.conclusion = new_content[0]
            else:
                if "=>" in new_content:
                    index = new_content.index("=>")
                    self.left = new_content[:index]
                    self.conclusion = new_content[-1]
                    for element in self.left:
                        if element not in LOGIC_OPERANDS:
                            self.premises.append(element)
                else:
                    self.conclusion = new_content[-1]
                    self.left = new_content[:-1]
                    for element in self.left:
                        if element not in LOGIC_OPERANDS:
                            self.premises.append(element)
                            
    def execute_logic_operation(self,operator, operand1, operand2):
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
        
    def evaluate(self, model):
        # Evaluate the truth value of the sentence under the given model.
        stack = []
        for token, value in model:
            if token in self.symbols:
                self.symbols[token] = value
        symbols_clone = self.symbols.copy()
        for token in self.content:
            if token not in LOGIC_OPERANDS:
                stack.append(token)
            elif len(stack) >= 2 and token != "~":
                right = stack.pop()
                left = stack.pop()
                symbols_clone[f"({left} {token} {right})"] = self.execute_logic_operation(token, symbols_clone[left], symbols_clone[right])
                stack.append(f"({left} {token} {right})")
            elif len(stack) >= 1 and token == "~":
                right = stack.pop()
                symbols_clone[f"~{right}"] = self.execute_logic_operation(token, symbols_clone[right], symbols_clone[right])
                stack.append(f"~{right}")
        return symbols_clone[stack.pop()]
    
    
    def __str__(self):
        return f"content {str(self.content)}, symbols {str(self.symbols)}"
    