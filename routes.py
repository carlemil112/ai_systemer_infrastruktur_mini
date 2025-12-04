from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# Request and reponse models
from models import ImageRequest, SemanticRequest, ClassificationResult, Top5Results

# Classifiers
from semantic import SemanticClassifier
from imageclassifier import ImageClassifier

# Database + api keys
from database import get_db, RequestLog
from security import get_current_api_key

# API endpoints version 1 and 2
v1 = APIRouter(prefix="/v1")
v2 = APIRouter(prefix="/v2")

# Loads the classifiers 
semantic_classifier = SemanticClassifier()
image_classifier = ImageClassifier()

# Returns list of available models
@v1.get("/models")
def list_models(api_key: str = Depends(get_current_api_key)):
    return {
        "models": [
            "sentiment-analysis",
            "image-classification",
            "image-classification-top5"
        ]
    }

@v1.post("/images", response_model=ClassificationResult)
def classify_image(
    req: ImageRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_current_api_key),
):
    try:
        # Runs image classifier
        label, conf = image_classifier.classify_image(req.image_base64)

        # Store request output in the database
        log = RequestLog(
            api_key=api_key,
            endpoint="images",
            input_text=None,
            predicted_label=label,
            confidence=conf,
        )
        db.add(log)
        db.commit()

        return ClassificationResult(label=label, confidence=conf)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@v1.post("/semantic", response_model=ClassificationResult)
def classify_semantic(
    req: SemanticRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_current_api_key),
):
    try:
        # Run semantic classifier
        label, conf = semantic_classifier.classify(req.text)

        # Store text, label and confidence in the database
        log = RequestLog(
            api_key=api_key,
            endpoint="semantic",
            input_text=req.text,
            predicted_label=label,
            confidence=conf,
        )
        db.add(log)
        db.commit()

        return ClassificationResult(label=label, confidence=conf)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@v2.post("/images", response_model=Top5Results)
def classify_image_v2(
    req: ImageRequest,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_current_api_key),
):
    try:
       # Run top-5 image classification 
        result = image_classifier.classify_top5(req.image_base64)

        # Stores the predicted list in the database
        log = RequestLog(
            api_key=api_key,
            endpoint="images_v2",
            input_text=None,
             predicted_label=str(result["predictions"]),
            confidence=None,
        )
        db.add(log)
        db.commit()
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


