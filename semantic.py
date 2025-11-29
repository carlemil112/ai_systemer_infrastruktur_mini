#dummy
class SemanticReviewClassifier:
    def __init__(self):
        self.labels = ["Good", "Bad"]

    def classify(self, image_base64: str):
        if "good" in image_base64.lower():
            return "Good", 0.95
        return "unknown", 0.10
