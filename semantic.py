from transformers import pipeline
# Semantic text classifier built on Hugging Faces's sentiment-analysis pipeline
class SemanticClassifier:
    def __init__(self):
        # Load of the pretrained pipeline. 
        self.model = pipeline("sentiment-analysis")

    def classify(self, text: str):
        try:
            # Inference on the text input. Returns a lable and confidence
            result = self.model(text)[0]
            label = result["label"]
            confidence = float(result["score"])
            return label, confidence
        except Exception:
            return "invalid_text", 0.0
