from app.database.database import Base
from sqlalchemy import Column, String, Integer, DateTime, func


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    answer = Column(String)
    created_at = Column(DateTime)
    collected_at = Column(DateTime, default=func.now())