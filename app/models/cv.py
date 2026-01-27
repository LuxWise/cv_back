from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Cv_personal_info(Base):
    __tablename__ = "cv_personal_info"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    localization = Column(String, nullable=True)
    about_me = Column(String, nullable=True)
    aspiration = Column(String, nullable=True)
    interests = Column(String, nullable=True)
    phone = Column(String, unique=True, index=True, nullable=True)
    photo = Column(String, unique=True, index=True, nullable=True)
    website = Column(String, unique=True, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True, nullable=False)

    user = relationship("User", back_populates="cv_personal_info", uselist=False)

class Cv_social_network(Base):
    __tablename__ = "cv_social_network"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    network_name = Column(String, nullable=False)
    profile_link = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="cv_social_networks")

class Cv_education(Base):
    __tablename__ = "cv_education"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    institution = Column(String, nullable=False)
    area = Column(String, nullable=False)
    degree = Column(String, nullable=False)
    start_date = Column(String, nullable=True)
    end_date = Column(String, nullable=True)
    location = Column(String, nullable=True)
    summary = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="cv_education")

class Cv_experience(Base):
    __tablename__ = "cv_experience"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    workplace = Column(String, nullable=False)
    position = Column(String, nullable=False)
    start_date = Column(String, nullable=True)
    end_date = Column(String, nullable=True)
    location = Column(String, nullable=True)
    summary = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="cv_experience")

    responsibilities = relationship(
        "Cv_experience_responsibilities",
        back_populates="experience",
    )
    achievements = relationship(
        "Cv_experience_achievements",
        back_populates="experience",
    )

class Cv_experience_responsibilities(Base):
    __tablename__ = "cv_experience_responsibilities"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    responsibility = Column(String, nullable=False)
    
    experience_id = Column(Integer, ForeignKey("cv_experience.id"), nullable=False)
    experience = relationship("Cv_experience", back_populates="responsibilities")

class Cv_experience_achievements(Base):
    __tablename__ = "cv_experience_achievements"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    achievement = Column(String, nullable=False)

    experience_id = Column(Integer, ForeignKey("cv_experience.id"), nullable=False)
    experience = relationship("Cv_experience", back_populates="achievements")

class Cv_project(Base):
    __tablename__ = "cv_project"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    start_date = Column(String, nullable=True)
    end_date = Column(String, nullable=True)
    description = Column(String, nullable=True)
    location = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="cv_project")

    achievements = relationship("Cv_project_achievements", back_populates="cv_project")

class Cv_project_achievements(Base):
    __tablename__ = "cv_project_achievements"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    achievement = Column(String, nullable=False)

    project_id = Column(Integer, ForeignKey("cv_project.id"), nullable=False)
    cv_project = relationship("Cv_project", back_populates="achievements")


class Cv_skill(Base):
    __tablename__ = "cv_skill"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    label = Column(String, nullable=False)
    detail = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", back_populates="cv_skill")