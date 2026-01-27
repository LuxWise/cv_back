from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import authGuard
from app.services import cv_services
from app.models.user import User
from app.schemas.cv import *

router = APIRouter()

# CV
@router.get('', response_model=CvResponse)
async def get_cv(
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.get_cv(db, current_user.id)
    return result

# CV Personal Info Endpoints
@router.get('/personal-info', response_model=CvPersonalInfoResponse)
async def get_cv_personal_info(
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.get_cv_personal_info(db, current_user.id)
    return result

@router.post('/personal-info', response_model=CvPersonalInfoResponse)
async def set_cv_personal_info( 
        data: CvPersonalInfoCreate, 
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.set_cv_personal_info(db, current_user.id, data)
    return result

@router.patch('/personal-info', response_model=CvPersonalInfoResponse)
async def patch_cv_personal_info( 
        data: CvPersonalInfoCreate, 
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.patch_cv_personal_info(db, current_user.id, data)
    return result

# CV Education Endpoints 
@router.get('/education', response_model=list[CvEducationResponse])
async def get_cv_education(
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.get_cv_education(db, current_user.id)
    return result

@router.post('/education', response_model=CvEducationResponse)
async def set_cv_education( 
        data: CvEducationCreate, 
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.set_cv_education(db, current_user.id, data)
    return result

@router.patch('/education', response_model=CvEducationResponse)
async def patch_cv_education( 
        data: CvEducationUpdate, 
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.patch_cv_education(db, current_user.id, data)
    return result

# CV Experience Endpoints 
@router.get('/experience', response_model=list[CvExperienceResponse])
async def get_cv_experience(
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.get_cv_experience(db, current_user.id)
    return result

@router.post('/experience', response_model=CvExperienceResponse)
async def set_cv_experience( 
        data: CvExperienceCreate, 
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.set_cv_experience(db, current_user.id, data)
    return result

@router.patch('/experience', response_model=CvExperienceResponse)
async def patch_cv_experience( 
        data: CvExperienceUpdate, 
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.patch_cv_experience(db, current_user.id, data)
    return result

@router.get('/experience/responsibilities', response_model=list[CvExperienceResponsibilitiesResponse])
async def get_cv_experience_responsibilities(
        experience_id: int,
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.get_cv_experience_responsibilities(db, current_user.id, experience_id)
    return result

@router.post('/experience/responsibilities', response_model=CvExperienceResponsibilitiesResponse)
async def set_cv_experience_responsibilities( 
        data: CvExperienceResponsibilitiesCreate, 
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.set_cv_experience_responsibilities(db, current_user.id, data)
    return result

@router.patch('/experience/responsibilities', response_model=CvExperienceResponsibilitiesResponse)
async def patch_cv_experience_responsibilities( 
        data: CvExperienceResponsibilitiesUpdate, 
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.patch_cv_experience_responsibilities(db, current_user.id, data)
    return result

@router.get('/experience/achievements', response_model=list[CvExperienceAchievementsResponse])
async def get_cv_experience_achievements(
        experience_id: int,
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.get_cv_experience_achievements(db, current_user.id, experience_id)
    return result

@router.post('/experience/achievements', response_model=CvExperienceAchievementsResponse)
async def set_cv_experience_achievements( 
        data: CvExperienceAchievementsCreate, 
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.set_cv_experience_achievements(db, current_user.id, data)
    return result

@router.patch('/experience/achievements', response_model=CvExperienceAchievementsResponse)
async def patch_cv_experience_achievements( 
        data: CvExperienceAchievementsUpdate, 
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.patch_cv_experience_achievements(db, current_user.id, data)
    return result

# CV Project Endpoints 
@router.get('/project', response_model=list[CvProjectResponse])
async def get_cv_project(
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.get_cv_project(db, current_user.id)
    return result

@router.post('/project', response_model=CvProjectResponse)
async def set_cv_project( 
        data: CvProjectCreate, 
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.set_cv_project(db, current_user.id, data)
    return result

@router.patch('/project', response_model=CvProjectResponse)
async def patch_cv_project( 
        data: CvProjectUpdate, 
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.patch_cv_project(db, current_user.id, data)
    return result

@router.get('/project/achievements', response_model=list[CvProjectAchievementsResponse])
async def get_cv_project_achievements(
        project_id: int,
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.get_cv_project_achievements(db, current_user.id, project_id)
    return result

@router.post('/project/achievements', response_model=CvProjectAchievementsResponse)
async def set_cv_project_achievements( 
        data: CvProjectAchievementsCreate, 
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.set_cv_project_achievements(db, current_user.id, data)
    return result

@router.patch('/project/achievements', response_model=CvProjectAchievementsResponse)
async def patch_cv_project_achievements( 
        data: CvProjectAchievementsUpdate, 
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.patch_cv_project_achievements(db, current_user.id, data)
    return result

# CV Project Endpoints 
@router.get('/skill', response_model=list[CvSkillResponse])
async def get_cv_skill(
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.get_cv_skill(db, current_user.id)
    return result

@router.post('/skill', response_model=CvSkillResponse)
async def set_cv_skill( 
        data: CvSkillCreate, 
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.set_cv_skill(db, current_user.id, data)
    return result

@router.patch('/skill', response_model=CvSkillResponse)
async def patch_cv_skill( 
        data: CvSkillUpdate, 
        db: Session = Depends(get_db), 
        current_user: User = Depends(authGuard)
    ):
    result = cv_services.patch_cv_skill(db, current_user.id, data)
    return result
