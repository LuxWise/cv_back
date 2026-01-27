from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String(128), nullable=False)
    api_key = Column(String, unique=True, index=True, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    cv_personal_info = relationship("Cv_personal_info", back_populates="user", uselist=False)
    cv_social_networks = relationship("Cv_social_network", back_populates="user")
    cv_education = relationship("Cv_education", back_populates="user")
    cv_experience = relationship("Cv_experience", back_populates="user")
    cv_project = relationship("Cv_project", back_populates="user")
    cv_skill = relationship("Cv_skill", back_populates="user")

class RegisteredUser(Base):
    __tablename__ = "registered_user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String(128), nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    two_fa = relationship("TwoFA", back_populates="user", uselist=False)

class TwoFA(Base):
    __tablename__ = "two_fa"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String, nullable=False)
    enabled = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("registered_user.id"), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    user = relationship("RegisteredUser", back_populates="two_fa", uselist=False)