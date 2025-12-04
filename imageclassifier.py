#Based on Huggin Faces example for microsoft/resnet-18 and adapted using ChatGPT: 
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch
import base64
import io
from typing import List

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

    def classify_top5(self, image_base64: str):
       

        try:
            image_bytes = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except Exception:
            return {
                "model": self.model_name,
                "top_k": 5,
                "predictions": []
            }

        inputs = self.processor(image, return_tensors="pt")

        with torch.no_grad():
            logits = self.model(**inputs).logits
            probs = torch.nn.functional.softmax(logits, dim=-1)[0]

        top5 = torch.topk(probs, k=5)

        predictions = []
        for score, idx in zip(top5.values, top5.indices):
            predictions.append({
                "label": self.model.config.id2label[int(idx)],
                "confidence": float(score)
            })

        return {
            "model": self.model_name,
            "top_k": 5,
            "predictions": predictions
        }


