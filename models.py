from pydantic import BaseModel

class ImageRequest(BaseModel):
    image_base64: str

class ReviewRequest(BaseModel):
    text: str

class ClassificationResult(BaseModel):
    label: str
    confidence: float

class Top5Prediction(BaseModel):
    label: str
    confidence: float


class Top5Result(BaseModel):
    model: str        
    top_k: int        
    predictions: List[Top5Prediction]
