from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from database import RequestLog
from security import get_current_api_key  # er igang med at lave
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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/classify-review", response_model=ClassificationResult)
def classify_review(
    req: ReviewRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_current_api_key),
):
    label, conf = review_classifier.classify_review(req.text)

    log = RequestLog(
        api_key=api_key,
        endpoint="classify-review",
        input_text=req.text,
        predicted_label=label,
        confidence=conf,
    )
    db.add(log)
    db.commit()

    return ClassificationResult(label=label, confidence=conf)
