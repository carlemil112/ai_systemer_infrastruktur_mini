from pydantic import BaseModel
from typing import List

# Rewuest model for image classification 
class ImageRequest(BaseModel):
    image_base64: str
# Request model for semantic classification 
class SemanticRequest(BaseModel):
    text: str
# Response model for classification results
class ClassificationResult(BaseModel):
    label: str
    confidence: float
# Single entry in top 5 output 
class Top5Prediction(BaseModel):
    label: str
    confidence: float
# Full response for top 5 image classifier. 
class Top5Results(BaseModel):
    model: str        
    top_k: int        
    predictions: List[Top5Prediction]
