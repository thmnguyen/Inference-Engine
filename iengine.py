import sys
from InferenceEngine import InferenceEngine
from KnowledgeBase import KnowledgeBase
from Algorithms.TruthTable import *
from Algorithms.FowardChaining import *
from Algorithms.BackwardChaining import *

def main():
    if len(sys.argv) <= 2:
        print("Invalid input")
        print("Usage: python main.py <input_file> <algorithm>")
        print("Algorithms: TT (Truth Table), FC (Forward Chaining), BC (Backward Chaining)")
        return
    else:
        file_name = sys.argv[1]
        algorithm_choice = sys.argv[2].upper()
        if algorithm_choice == "TT":
            knowledge_base = KnowledgeBase(False)
            knowledge_base.load_input_file(file_name)
            algorithm = TruthTableAlgorithm(knowledge_base)
        elif algorithm_choice == "FC":
            knowledge_base = KnowledgeBase(True)
            knowledge_base.load_input_file(file_name)
            algorithm = ForwardChainingAlgorithm(knowledge_base)
        elif algorithm_choice == "BC":
            knowledge_base = KnowledgeBase(True)
            knowledge_base.load_input_file(file_name)
            algorithm = BackwardChainingAlgorithm(knowledge_base)
        else:
            print("Invalid algorithm choice")
            return
        engine = InferenceEngine(algorithm)
        engine.run_inference()

if __name__ == "__main__":
    main()