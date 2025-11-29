from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import ImageRequest, ReviewRequest, ClassificationResult
from semantic import SemanticReviewClassifier
from imageclassifier import ImageClassifier

#database + api nøgler
from database import get_db, RequestLog
from security import get_current_api_key

router = APIRouter(prefix="/v1")

review_classifier = SemanticReviewClassifier()
image_classifier = ImageClassifier()


@router.post("/classify-image", response_model=ClassificationResult)
def classify_image(
    req: ImageRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_current_api_key),
):

    label, conf = image_classifier.classify_image(req.image_base64)

    # log i databasen (gemmer ikke hele billedet, kun output)
    log = RequestLog(
        api_key=api_key,
        endpoint="classify-image",
        input_text=None,
        predicted_label=label,
        confidence=conf,
    )
    db.add(log)
    db.commit()

    return ClassificationResult(label=label, confidence=conf)


@router.post("/classify-review", response_model=ClassificationResult)
def classify_review(
    req: ReviewRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_current_api_key),
):
    label, conf = review_classifier.classify(req.text)

    # log request+output
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
