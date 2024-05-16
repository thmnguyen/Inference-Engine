from LogicSentence import LogicSentence
from utils import *

class KnowledgeBase:
    def __init__(self):
        self.sentences = []
        self.symbols = dict()
        self.query = []
        self.query_symbols = dict()
        self.current_action = "TELL"

    def add_sentence(self, sentence: str):
        
        # Add a sentence to the knowledge base.
        post_fix = infix_to_postfix(sentence)
        
        sentence_symbols = self.add_symbol(post_fix, True)
        self.sentences.append(LogicSentence(sentence, post_fix, sentence_symbols))

    def add_query(self, query: str):
        # Add a query to the knowledge base.
        post_fix = infix_to_postfix(query)
        sentence_symbols = self.add_symbol(post_fix, False)
        self.query.append(LogicSentence(query, post_fix, sentence_symbols))

    def add_symbol(self, sequence: str, is_sentence: bool) -> dict():
        # Add symbols to the knowledge base or query.
        sentence_symbols = dict()
        for symbol in sequence:
            if symbol not in LOGIC_OPERANDS and symbol not in sentence_symbols:
                sentence_symbols[symbol] = True
                if is_sentence:
                    if symbol not in self.symbols:
                        self.symbols[symbol] = True
                else:
                    if symbol not in self.query_symbols:
                        self.query_symbols[symbol] = False
        return sentence_symbols

    def process_command(self, command):
        # Process a command (sentence or query) based on the current action.
        if self.current_action == "TELL":
            self.add_sentence(command)
        elif self.current_action == "ASK":
            self.add_query(command)

    def set_action(self, action):
        # Set the current action (TELL or ASK).
        if action == "TELL":
            self.current_action = "TELL"
        elif action == "ASK":
            self.current_action = "ASK"
    
    def load_input_file(self, file_name):
        # Load input from a file and populate the knowledge base.
        try:
            with open(file_name, "r", encoding="utf8") as file:
                lines = file.read().splitlines()
                for line in lines:
                    if line == "TELL":
                        self.set_action("TELL")
                    elif line == "ASK":
                        self.set_action("ASK")
                    else:
                        sentences = line.split(";")
                        for sequence in sentences:
                            sequence = sequence.strip().replace(" ", "")
                            if sequence == "":
                                continue
                            else:
                                self.process_command(sequence)
                file.close()
                return self
        except IOError:
            print("File not found")
            return

    def is_model_valid(self, model):
        # Check if a model satisfies all sentences in the knowledge base.
        for sentence in self.sentences:
            if not sentence.evaluate(model):
                return False
        return True