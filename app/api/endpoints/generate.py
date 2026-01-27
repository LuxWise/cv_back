from fastapi import APIRouter, Depends
from huggingface_hub import User
from requests import Session
from app.core.auth import authGuard
from app.core.database import get_db
from app.services.generate_cv_services import generate_cv, generate_cv_ia
from app.schemas.generate import CvGenerateAIRequest

router = APIRouter()

@router.get('')
async def cv_generate_cv(
    db: Session = Depends(get_db), 
    current_user: User = Depends(authGuard)
    ):
    cv_json = generate_cv(db=db, user_id=current_user.id)
    if cv_json is None:
        return {"detail": "Error generating CV"}
    return {"cv": cv_json}

@router.post('/ia')
async def cv_generate_cv_ia(
    job_offer: CvGenerateAIRequest,
    db: Session = Depends(get_db), 
    current_user: User = Depends(authGuard),
    ):

    cv_json = generate_cv_ia(db=db, user_id=current_user.id, job_offer=job_offer)
    if cv_json is None:
        return {"detail": "Error generating CV"}
    return {"cv": cv_json}
