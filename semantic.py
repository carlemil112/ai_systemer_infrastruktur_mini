from transformers import pipeline

class SemanticReviewClassifier:
    def __init__(self):
        self.model = pipeline(
            "sentiment-analysis",
            model="distilbert/distilbert-base-uncased"
)


    def classify(self, text: str):

        try:
            result = self.model(text)[0]
            label = result["label"]
            confidence = float(result["score"])
            return label, confidence
        except Exception:
            return "invalid_text", 0.0
