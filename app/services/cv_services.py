from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from app.models.cv import *
from app.models.user import User
from app.schemas.cv import *

# Service functions for CV
def get_cv(db: Session, user_id: int):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        personal_info = db.query(Cv_personal_info).filter(Cv_personal_info.user_id == user_id).first()
        education = db.query(Cv_education).filter(Cv_education.user_id == user_id).all()
        experience = (
            db.query(Cv_experience)
            .options(
                joinedload(Cv_experience.responsibilities),  
                joinedload(Cv_experience.achievements),      
            )
            .filter(Cv_experience.user_id == user_id)
            .all() 
        )
        project = (
            db.query(Cv_project)
            .options(
                joinedload(Cv_project.achievements),      
            )
            .filter(Cv_project.user_id == user_id)
            .all() 
        )
        skills = db.query(Cv_skill).filter(Cv_skill.user_id == user_id).all()

        if not personal_info:
            raise HTTPException(status_code=404, detail="CV not found")

        basic_info = BasicInfoResponse(
            email=user.email,
            first_name=user.firstname,
            last_name=user.lastname
        )

        cv_data = CvResponse(
            basic_info=basic_info,
            personal_info=personal_info,
            education=education,
            experience=experience,
            projects=project,
            skills=skills
        )

        return cv_data
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error persisting CV.")
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

# Service functions for CV Personal Info
def get_cv_personal_info(db: Session, user_id: int):
    result = db.query(Cv_personal_info).filter(Cv_personal_info.user_id == user_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="CV personal info not found")
    
    return result

def set_cv_personal_info(db: Session, user_id: int, data: CvPersonalInfoCreate):
    try:
        existing_info = db.query(Cv_personal_info).filter(
            Cv_personal_info.phone == data.phone,
            Cv_personal_info.photo == data.photo,
            Cv_personal_info.website == data.website,
        ).first()

        if existing_info:
            raise HTTPException(
                status_code=400,
                detail="CV personal info already exists with the same phone, photo or website.",
            )        

        personal_info = db.query(Cv_personal_info).filter(Cv_personal_info.user_id == user_id).first()
        if personal_info:
            data_dict = data.model_dump(exclude_unset=True)
            for key, value in data_dict.items():
                setattr(personal_info, key, value)
            db.commit()
            db.refresh(personal_info)
            return personal_info
        else:
            new_info = Cv_personal_info(
                user_id=user_id,
                localization=data.localization,
                about_me=data.about_me,
                aspiration=data.aspiration,
                interests=data.interests,
                phone=data.phone,
                photo=data.photo,
                website=data.website,
            )
            db.add(new_info)
            db.commit()
            db.refresh(new_info)
            return new_info
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error persisting CV personal info.",
        )
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

def patch_cv_personal_info(db: Session, user_id: int, data: CvPersonalInfoCreate):
    try:
        existing_info = db.query(Cv_personal_info).filter(
            Cv_personal_info.phone == data.phone,
            Cv_personal_info.photo == data.photo,
            Cv_personal_info.website == data.website,
        ).first()
        if existing_info and existing_info.user_id != user_id:
            raise HTTPException(
                status_code=400,
                detail="Another CV personal info already exists with the same phone, photo or website.",
            )

        personal_info = db.query(Cv_personal_info).filter(Cv_personal_info.user_id == user_id).first()
        if not personal_info:
            raise HTTPException(status_code=404, detail="CV personal info not found")

        data_dict = data.model_dump(exclude_unset=True)
        for key, value in data_dict.items():
            setattr(personal_info, key, value)
        db.commit()
        db.refresh(personal_info)
        return personal_info

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error persisting CV personal info.",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

# Service functions for CV Education
def get_cv_education(db: Session, user_id: int):
    try:
        result = (
            db.query(Cv_education)
            .filter(Cv_education.user_id == user_id)
            .all()
        )
        if not result:
            raise HTTPException(status_code=404, detail="CV education not found")
        
        return result
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error persisting CV education.")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

def set_cv_education(db: Session, user_id: int, data: CvEducationCreate):
    try: 
        duplicate = (
            db.query(Cv_education)
            .filter(
                Cv_education.user_id == user_id,
                Cv_education.institution == data.institution,
                Cv_education.degree == data.degree,
                Cv_education.start_date == data.start_date,
                Cv_education.end_date == data.end_date,
            )
            .first()
        )

        if duplicate:
            raise HTTPException(
                status_code=400,
                detail="Already exists an education entry with the same information.",
            )
        
        new_info = Cv_education(
            user_id=user_id,
            institution=data.institution,
            area=data.area,
            degree=data.degree,
            start_date=data.start_date,
            end_date=data.end_date,
            location=data.location,
            summary=data.summary,
        )
        db.add(new_info)
        db.commit()
        db.refresh(new_info)
        return new_info
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error persisting CV education.",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

def patch_cv_education(db: Session, user_id: int, data: CvEducationUpdate):
    try:
        existing_info =(
            db.query(Cv_education)
            .filter(Cv_education.user_id == user_id, Cv_education.id == data.education_id)
            .first()
        )
        
        if not existing_info:
            raise HTTPException(status_code=404, detail="CV education not found")

        data_dict = data.model_dump(exclude_unset=True)
        for key, value in data_dict.items():
            setattr(existing_info, key, value)
        db.commit()
        db.refresh(existing_info)
        return existing_info
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error persisting CV education.",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

# Service functions for CV Experience
def get_cv_experience(db: Session, user_id: int):
    try:
        result = (
            db.query(Cv_experience)
            .options(
                joinedload(Cv_experience.responsibilities),  
                joinedload(Cv_experience.achievements),      
            )
            .filter(Cv_experience.user_id == user_id)
            .all() 
        )

        if not result:
            raise HTTPException(status_code=404, detail="CV experience not found")

        return result
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error persisting CV experience.")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

def set_cv_experience(db: Session, user_id: int, data: CvExperienceCreate):
    try:
        duplicate = (
            db.query(Cv_experience)
            .filter(
                Cv_experience.user_id == user_id,
                Cv_experience.workplace == data.workplace,
                Cv_experience.position == data.position,
                Cv_experience.start_date == data.start_date,
                Cv_experience.end_date == data.end_date,
            )
            .first()
        )

        if duplicate:
            raise HTTPException(
                status_code=400,
                detail="Already exists an experience entry with the same information.",
            )

        new_info = Cv_experience(
            user_id=user_id,
            workplace=data.workplace,
            position=data.position,
            start_date=data.start_date,
            end_date=data.end_date,
            location=data.location,
            summary=data.summary,
        )
        db.add(new_info)
        db.commit()
        db.refresh(new_info)
        return new_info
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error persisting CV experience.",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

def patch_cv_experience(db: Session, user_id: int, data: CvExperienceUpdate):
    try:
        existing_info =( 
            db.query(Cv_experience)
            .filter(Cv_experience.user_id == user_id, Cv_experience.id == data.experience_id)
            .first()
        )
        if not existing_info:
            raise HTTPException(status_code=404, detail="CV experience not found")

        data_dict = data.model_dump(exclude_unset=True)
        for key, value in data_dict.items():
            setattr(existing_info, key, value)
        db.commit()
        db.refresh(existing_info)
        return existing_info
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error persisting CV experience.",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

def get_cv_experience_responsibilities(db: Session, user_id: int, experience_id: int):
    try:
        experience = (
            db.query(Cv_experience)
            .filter(Cv_experience.user_id == user_id, Cv_experience.id == experience_id)
            .first()
        )

        if not experience:
            raise HTTPException(status_code=404, detail="CV experience responsibilities are not available for this user")
        
        result = (
            db.query(Cv_experience_responsibilities)
            .filter(Cv_experience_responsibilities.experience_id == experience_id)
            .all()
        )

        if not result:
            raise HTTPException(status_code=404, detail="CV experience responsibilities not found")
        return result
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error persisting CV experience responsibilities.")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

def set_cv_experience_responsibilities(db: Session, user_id: int, data: CvExperienceResponsibilitiesCreate):
    try:
        experience = (
            db.query(Cv_experience)
            .filter(Cv_experience.user_id == user_id, Cv_experience.id == data.experience_id)
            .first()
        )

        if not experience:
            raise HTTPException(status_code=404, detail="CV experience responsibilities are not available for this user")

        duplicate = (
            db.query(Cv_experience_responsibilities)
            .filter(
                Cv_experience_responsibilities.experience_id == data.experience_id,
                Cv_experience_responsibilities.responsibility == data.responsibility,
            )
            .first()
        )

        if duplicate:
            raise HTTPException(
                status_code=400,
                detail="Already exists a responsibility entry with the same information for this experience.",
            )

        new_info = Cv_experience_responsibilities(
            responsibility=data.responsibility,
            experience_id=data.experience_id,
        )
        db.add(new_info)
        db.commit()
        db.refresh(new_info)
        return new_info
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error persisting CV experience responsibilities.",
        )
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

def patch_cv_experience_responsibilities(db: Session, user_id: int, data: CvExperienceResponsibilitiesUpdate):
    try:
        experience = (
            db.query(Cv_experience)
            .filter(Cv_experience.user_id == user_id, Cv_experience.id == data.experience_id)
            .first()
        )

        if not experience:
            raise HTTPException(status_code=404, detail="CV experience responsibilities are not available for this user")

        existing_info = (
            db.query(Cv_experience_responsibilities)
            .filter(Cv_experience_responsibilities.experience_id == data.experience_id, Cv_experience_responsibilities.id == data.responsibility_id)
            .first()
        )
        if not existing_info:
            raise HTTPException(status_code=404, detail="CV experience responsibilities not found")

        data_dict = data.model_dump(exclude_unset=True)
        for key, value in data_dict.items():
            setattr(existing_info, key, value)
        db.commit()
        db.refresh(existing_info)
        return existing_info
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error persisting CV experience responsibilities.",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

def get_cv_experience_achievements(db: Session, user_id: int,experience_id: int):
    try:
        experience = (
            db.query(Cv_experience)
            .filter(Cv_experience.user_id == user_id, Cv_experience.id == experience_id)
            .first()
        )

        if not experience:
            raise HTTPException(status_code=404, detail="CV experience achievements are not available for this user")
        
        result = (
            db.query(Cv_experience_achievements)
            .filter(Cv_experience_achievements.experience_id == experience_id)
            .all()
        )

        if not result:
            raise HTTPException(status_code=404, detail="CV experience achievements not found")
        return result
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error persisting CV experience achievements.")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

def set_cv_experience_achievements(db: Session, user_id: int, data: CvExperienceAchievementsCreate):
    try:
        experience = (
            db.query(Cv_experience)
            .filter(Cv_experience.user_id == user_id, Cv_experience.id == data.experience_id)
            .first()
        )

        if not experience:
            raise HTTPException(status_code=404, detail="CV experience achievements are not available for this user")

        duplicate = (
            db.query(Cv_experience_achievements)
            .filter(
                Cv_experience_achievements.experience_id == data.experience_id,
                Cv_experience_achievements.achievement == data.achievement,
            )
            .first()
        )

        if duplicate:
            raise HTTPException(
                status_code=400,
                detail="Already exists an achievement entry with the same information for this experience.",
            )

        new_info = Cv_experience_achievements(
            achievement=data.achievement,
            experience_id=data.experience_id,
        )
        db.add(new_info)
        db.commit()
        db.refresh(new_info)
        return new_info
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error persisting CV experience achievements.",
        )
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

def patch_cv_experience_achievements(db: Session, user_id: int, data: CvExperienceAchievementsUpdate):
    try:
        experience = (
            db.query(Cv_experience)
            .filter(Cv_experience.user_id == user_id, Cv_experience.id == data.experience_id)
            .first()
        )

        if not experience:
            raise HTTPException(status_code=404, detail="CV experience achievements are not available for this user")

        existing_info = (
            db.query(Cv_experience_achievements)
            .filter(Cv_experience_achievements.experience_id == data.experience_id, Cv_experience_achievements.id == data.achievement_id)
            .first()
        )
        if not existing_info:
            raise HTTPException(status_code=404, detail="CV experience achievements not found")

        data_dict = data.model_dump(exclude_unset=True)
        for key, value in data_dict.items():
            setattr(existing_info, key, value)
        db.commit()
        db.refresh(existing_info)
        return existing_info
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error persisting CV experience achievements.",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

# Service functions for CV Project
def get_cv_project(db: Session, user_id: int):
    try:
        result = ( 
            db.query(Cv_project)
            .options(
                joinedload(Cv_project.achievements),      
            )
            .filter(Cv_project.user_id == user_id)
            .all() 
        )

        if not result:
            raise HTTPException(status_code=404, detail="CV project not found")

        return result
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error persisting CV project.")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

def set_cv_project(db: Session, user_id: int, data: CvProjectCreate):
    try:
        duplicate = (
            db.query(Cv_project)
            .filter(
                Cv_project.user_id == user_id,
                Cv_project.name == data.name,
                Cv_project.start_date == data.start_date,
                Cv_project.end_date == data.end_date,
                Cv_project.description == data.description,
            )
            .first()
        )

        if duplicate:
            raise HTTPException(
                status_code=400,
                detail="Already exists a project entry with the same information.",
            )

        new_info = Cv_project(
            user_id=user_id,
            name=data.name,
            start_date=data.start_date,
            end_date=data.end_date,
            description=data.description,
            location=data.location
        )
        db.add(new_info)
        db.commit()
        db.refresh(new_info)
        return new_info
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error persisting CV project.",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

def patch_cv_project(db: Session, user_id: int, data: CvProjectUpdate):
    try:
        existing_info =( 
            db.query(Cv_project)
            .filter(Cv_project.user_id == user_id, Cv_project.id == data.project_id)
            .first()
        )
        if not existing_info:
            raise HTTPException(status_code=404, detail="CV project not found")

        data_dict = data.model_dump(exclude_unset=True)
        for key, value in data_dict.items():
            setattr(existing_info, key, value)
        db.commit()
        db.refresh(existing_info)
        return existing_info
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error persisting CV project.",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

def get_cv_project_achievements(db: Session, user_id: int, project_id: int):
    try:
        project = (
            db.query(Cv_project)
            .filter(Cv_project.user_id == user_id, Cv_project.id == project_id)
            .first()
        )

        if not project:
            raise HTTPException(status_code=404, detail="CV project its not available for this user")
        
        result = (
            db.query(Cv_project_achievements)
            .filter(Cv_project_achievements.project_id == project_id)
            .all()
        )

        if not result:
            raise HTTPException(status_code=404, detail="CV project achievements not found")

        return result
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error persisting CV project achievements.")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

def set_cv_project_achievements(db: Session, user_id: int, data: CvProjectAchievementsCreate):
    try:
        project = (
            db.query(Cv_project)
            .filter(Cv_project.user_id == user_id, Cv_project.id == data.project_id)
            .first()
        )

        if not project:
            raise HTTPException(status_code=404, detail="CV project achievements are not available for this user")

        duplicate = (
            db.query(Cv_project_achievements)
            .filter(
                Cv_project_achievements.project_id == data.project_id,
                Cv_project_achievements.achievement == data.achievement,
            )
            .first()
        )

        if duplicate:
            raise HTTPException(
                status_code=400,
                detail="Already exists an achievement entry with the same information for this project.",
            )

        new_info = Cv_project_achievements(
            achievement=data.achievement,
            project_id=data.project_id,
        )
        db.add(new_info)
        db.commit()
        db.refresh(new_info)
        return new_info
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error persisting CV project achievements.",
        )
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

def patch_cv_project_achievements(db: Session, user_id: int, data: CvProjectAchievementsUpdate):
    try:
        project = (
            db.query(Cv_project)
            .filter(Cv_project.user_id == user_id, Cv_project.id == data.project_id)
            .first()
        )

        if not project:
            raise HTTPException(status_code=404, detail="CV project achievements are not available for this user")

        existing_info = (
            db.query(Cv_project_achievements)
            .filter(Cv_project_achievements.project_id == data.project_id, Cv_project_achievements.id == data.achievement_id)
            .all()
        )
        if not existing_info:
            raise HTTPException(status_code=404, detail="CV project achievement not found")

        data_dict = data.model_dump(exclude_unset=True)
        for key, value in data_dict.items():
            setattr(existing_info, key, value)
        db.commit()
        db.refresh(existing_info)
        return existing_info
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error persisting CV project achievement.",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

# Service functions for CV Skills
def get_cv_skill(db: Session, user_id: int):
    try:
        result = ( 
            db.query(Cv_skill)
            .filter(Cv_skill.user_id == user_id)
            .all() 
        )

        if not result:
            raise HTTPException(status_code=404, detail="CV skill not found")

        return result
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error persisting CV skill.")
    except HTTPException:
        raise
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Internal server error")

def set_cv_skill(db: Session, user_id: int, data: CvSkillCreate):
    try:
        duplicate = (
            db.query(Cv_skill)
            .filter(
                Cv_skill.label == data.label,
                Cv_skill.detail == data.detail,
                Cv_skill.user_id == user_id,
            )
            .first()
        )

        if duplicate:
            raise HTTPException(
                status_code=400,
                detail="Already exists a skill entry with the same information.",
            )

        new_info = Cv_skill(
            user_id=user_id,
            label=data.label,
            detail=data.detail            
        )
        db.add(new_info)
        db.commit()
        db.refresh(new_info)
        return new_info
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error persisting CV skill.",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

def patch_cv_skill(db: Session, user_id: int, data: CvSkillUpdate):
    try:
        existing_info =( 
            db.query(Cv_skill)
            .filter(Cv_skill.user_id == user_id, Cv_skill.id == data.skill_id)
            .first()
        )
        if not existing_info:
            raise HTTPException(status_code=404, detail="CV project not found")

        data_dict = data.model_dump(exclude_unset=True)
        for key, value in data_dict.items():
            setattr(existing_info, key, value)
        db.commit()
        db.refresh(existing_info)
        return existing_info
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error persisting CV project.",
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
