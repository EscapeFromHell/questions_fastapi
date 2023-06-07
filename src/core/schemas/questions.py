from datetime import datetime

from pydantic import BaseModel, PositiveInt


class QuestionBase(BaseModel):
    question_id: PositiveInt
    question: str
    answer: str
    created_at: datetime


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(QuestionBase):
    pass


class QuestionInDB(QuestionBase):
    id: PositiveInt

    class Config:
        orm_mode = True


class Question(QuestionInDB):
    pass
