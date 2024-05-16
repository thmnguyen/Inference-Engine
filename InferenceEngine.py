from KnowledgeBase import KnowledgeBase
from Algorithms.InferenceAlgorithm import InferenceAlgorithm

class InferenceEngine:
    def __init__(self, algorithm: InferenceAlgorithm):
        self.algorithm = algorithm

    def run_inference(self):
        # Run the inference algorithm and print the result.
        result, count = self.algorithm.entails()
        if result:
            print(f"YES: {count}")
        else:
            print("NO")