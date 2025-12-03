from pydantic import BaseModel
from typing import List

class ImageRequest(BaseModel):
    image_base64: str

class SemanticRequest(BaseModel):
    text: str

class ClassificationResult(BaseModel):
    label: str
    confidence: float

class Top5Prediction(BaseModel):
    label: str
    confidence: float


class Top5Results(BaseModel):
    model: str        
    top_k: int        
    predictions: List[Top5Prediction]
