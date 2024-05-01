from utils import execute_logic_operation
from constants import LOGIC_OPERANDS

class LogicSentence:
    def __init__(self, raw_content: str = "", content: list = [], symbols: dict = dict()):
        self.raw_content = raw_content
        self.content = content
        self.symbols = symbols

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
            elif stack.__len__() >= 2 and token != "~":
                right = stack.pop()
                left = stack.pop()
                symbols_clone[f"({left} {token} {right})"] = execute_logic_operation(token, symbols_clone[left], symbols_clone[right])
                stack.append(f"({left} {token} {right})")
            elif stack.__len__() >= 1 and token == "~":
                right = stack.pop()
                symbols_clone[f"~{right}"] = execute_logic_operation(token, symbols_clone[right], symbols_clone[right])
                stack.append(f"~{right}")
        return symbols_clone[stack.pop()]

    def __str__(self) -> str:
        return f"content {str(self.content)}, symbols {str(self.symbols)}"