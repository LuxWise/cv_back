from typing import Optional, List
from pydantic import BaseModel, ConfigDict, EmailStr

class BasicInfoResponse(BaseModel):
    email: EmailStr
    first_name: str 
    last_name: str

    model_config = ConfigDict(from_attributes=True)

# CV Schemas
class CvResponse(BaseModel):
    basic_info: BasicInfoResponse
    personal_info: Optional['CvPersonalInfoResponse'] = None
    education: List['CvEducationResponse'] = []
    experience: List['CvExperienceResponse'] = []
    projects: List['CvProjectResponse'] = []
    skills: List['CvSkillResponse'] = []

    model_config = ConfigDict(from_attributes=True)

# CV Personal Info Schemas
class CvPersonalInfoCreate(BaseModel):
    localization: Optional[str] = None
    about_me: Optional[str] = None
    aspiration: Optional[str] = None
    interests: Optional[str] = None
    phone: Optional[str] = None
    photo: Optional[str] = None
    website: Optional[str] = None

class CvPersonalInfoResponse(BaseModel):
    localization: Optional[str] = None
    about_me: Optional[str] = None
    aspiration: Optional[str] = None
    interests: Optional[str] = None
    phone: Optional[str] = None
    photo: Optional[str] = None
    website: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# CV Education Schemas
class CvEducationCreate(BaseModel):
    institution: str
    area: Optional[str] = None
    degree: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None

class CvEducationUpdate(BaseModel):
    education_id: int
    institution: Optional[str] = None
    area: Optional[str] = None
    degree: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None

class CvEducationResponse(BaseModel):
    institution: str
    area: Optional[str] = None
    degree: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# CV Experience Schemas
class CvExperienceResponsibilitiesCreate(BaseModel):
    experience_id: int
    responsibility: str

class CvExperienceResponsibilitiesUpdate(BaseModel):
    responsibility_id: int
    experience_id: int
    responsibility: str

class CvExperienceResponsibilitiesResponse(BaseModel):
    responsibility: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class CvExperienceAchievementsCreate(BaseModel):
    experience_id: int
    achievement: str

class CvExperienceAchievementsUpdate(BaseModel):
    achievement_id: int
    experience_id: int
    achievement: str

class CvExperienceAchievementsResponse(BaseModel):
    achievement: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class CvExperienceCreate(BaseModel):
    workplace: str
    position: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None

class CvExperienceUpdate(BaseModel):
    experience_id: int
    workplace: Optional[str] = None
    position: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None

class CvExperienceResponse(BaseModel):
    workplace: str
    position: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    responsibilities: List[CvExperienceResponsibilitiesResponse] = []
    achievements: List[CvExperienceAchievementsResponse] = []

    model_config = ConfigDict(from_attributes=True)

# CV Project Schemas
class CvProjectAchievementsCreate(BaseModel):
    project_id: int
    achievement: Optional[str] = None

class CvProjectAchievementsUpdate(BaseModel):
    achievement_id: int
    project_id: int
    achievement: Optional[str] = None

class CvProjectAchievementsResponse(BaseModel):
    achievement: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class CvProjectCreate(BaseModel):
    name: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None

class CvProjectUpdate(BaseModel):
    project_id: int
    name: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None

class CvProjectResponse(BaseModel):
    name: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    achievements: List[CvProjectAchievementsResponse] = []

    model_config = ConfigDict(from_attributes=True)

# CV Skill Schemas
class CvSkillCreate(BaseModel):
    label: Optional[str] = None
    detail: Optional[str] = None

class CvSkillUpdate(BaseModel):
    skill_id: int
    label: Optional[str] = None
    detail: Optional[str] = None

class CvSkillResponse(BaseModel):
    label: Optional[str] = None
    detail: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)