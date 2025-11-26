from fastapi import APIRouter
from models import ImageRequest, ReviewRequest, ClassificationResult
from semantic import SemanticReviewClassifier # skal tilpasses vores modeller
from imageclassifier import ImageClassifier

router = APIRouter(prefix="/v1")

review_classifier = SemanticReviewClassifier()
image_classifier = ImageClassifier()
# Navne afhængigt af hvordan vores modeller ser ud. Mangler error handling.
@router.post("/classify-image", response_model=ClassificationResult)
def classify(req: ImageRequest):
    label, conf = image_classifier.classify_image(req.image_base64)
    return ClassificationResult(label=label, confidence=conf)
#Afhængigt af hvilke modeller vi bruger. 
@router.post("/classify-review", response_model=ClassificationResult)
def classify_review(req: ReviewRequest):
    label, conf = review_classifier.classify_review(req.text)
    return ClassificationResult(label=label, confidence=conf)