import base64
#dummy
class ImageClassifier:
    def __init__(self):
        self.labels = ["cat", "dog", "car", "unknown"]
    def classify(self, image_base64: str):
        try:
            decoded = base64.b64decode(image_base64)
        except Exception:
            return "invalid_image", 0.0
        size = len(decoded)

        if size < 5000:
            return "cat", 0.85
        elif size < 15000:
            return "dog", 0.80
        elif size < 50000:
            return "car", 0.75

        return "unknown", 0.10

