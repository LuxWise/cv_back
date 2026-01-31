from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Logging(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String, nullable=False)
    operation = Column(String, nullable=False)
    message = Column(String, nullable=False)
    http_method = Column(String, nullable=True)
    http_url = Column(String, nullable=True)
    requestHeaders = Column(String, nullable=True)
    requestBody = Column(String, nullable=True)
    requestStatus = Column(Integer, nullable=True)
    responseHeaders = Column(String, nullable=True)
    responseBody = Column(String, nullable=True)
    requestTime = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())