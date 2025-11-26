from pydantic import BaseModel

class ImageRequest(BaseModel):
    image_base64: str

class ReviewRequest(BaseModel):
    text: str

class ClassificationResult(BaseModel):
    label: str
    confidence: float
