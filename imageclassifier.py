from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch
import base64
import io

class ImageClassifier:
    def __init__(self):
        self.model_name = "microsoft/resnet-18"
        self.processor = AutoImageProcessor.from_pretrained(self.model_name)
        self.model = AutoModelForImageClassification.from_pretrained(self.model_name)

    def classify(self, image_base64: str):

        try:
            image_bytes = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except Exception:
            return "invalid_image", 0.0

        inputs = self.processor(image, return_tensors="pt")

        with torch.no_grad():
            logits = self.model(**inputs).logits

        predicted_class_id = int(logits.argmax(-1).item())
        label = self.model.config.id2label[predicted_class_id]

        confidence = float(
            torch.nn.functional.softmax(logits, dim=-1)[0][predicted_class_id]
        )

        return label, confidence
    def classify_image(self, image_base64: str):
        return self.classify(image_base64)

