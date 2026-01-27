from pydantic import BaseModel, ConfigDict, EmailStr

class CvGenerateAIRequest(BaseModel):
    job_offer: str

