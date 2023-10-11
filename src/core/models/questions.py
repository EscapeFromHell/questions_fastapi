from sqlalchemy import TIMESTAMP, Column, Integer, String

from src.core.models.base import Base


class Question(Base):
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, nullable=False, unique=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
