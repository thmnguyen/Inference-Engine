from utils import*
from constants import LOGIC_OPERANDS

class LogicSentence:
    def __init__(self, raw_content: str = "", content: list = [], symbols: dict = dict()):
        self.raw_content = raw_content
        self.content = content
        self.symbols = symbols
        self.premises = []
        self.set_variables()
        print(self.premises)

    def set_variables(self):
            new_content = get_tokens(self.raw_content)
            if len(new_content) == 0:
                self.conclusion = ""
            elif len(new_content) == 1:
                self.conclusion = new_content[0]
            else:
                self.conclusion = new_content[-1]
                index = new_content.index("=>")
                self.left = new_content[:index]
                for element in self.left:
                    if element not in LOGIC_OPERANDS:
                        self.premises.append(element)

    def evaluate(self, model: list[tuple[str, bool]]) -> bool:
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
                symbols_clone[f"({left} {token} {right})"] = execute_logic_operation(token, symbols_clone[left], symbols_clone[right])
                stack.append(f"({left} {token} {right})")
            elif len(stack) >= 1 and token == "~":
                right = stack.pop()
                symbols_clone[f"~{right}"] = execute_logic_operation(token, symbols_clone[right], symbols_clone[right])
                stack.append(f"~{right}")
        return symbols_clone[stack.pop()]

    def __str__(self) -> str:
        return f"content {str(self.content)}, symbols {str(self.symbols)}"