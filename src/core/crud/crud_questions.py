from typing import Sequence

from sqlalchemy.orm import Session

from src.core.crud import CRUDBase
from src.core.models import Question
from src.core.schemas import QuestionCreate, QuestionUpdate


class CRUDQuestion(CRUDBase[Question, QuestionCreate, QuestionUpdate]):
    def get_questions(self, db: Session, questions_id: list[int]) -> Sequence[Question]:
        """Возвращает вопросы из БД."""
        return db.query(self.model).where(self.model.question_id.in_(questions_id)).all()

    def get_last_question(self, db: Session) -> Question:
        """Возвращает последний добавленный в БД вопрос."""
        return db.query(self.model).order_by(self.model.id.desc()).first()


crud_questions = CRUDQuestion(Question)
