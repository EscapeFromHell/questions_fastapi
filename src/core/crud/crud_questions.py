from sqlalchemy import exists
from sqlalchemy.orm import Session

from src.core.crud import CRUDBase
from src.core.models import Question
from src.core.schemas import QuestionCreate, QuestionUpdate


class CRUDQuestion(CRUDBase[Question, QuestionCreate, QuestionUpdate]):
    def question_exists(self, db: Session, question_id: int) -> bool:
        """
        Проверяет наличие вопроса в БД по его идентификатору.

        :param db: Сессия базы данных
        :param question_id: Идентификатор вопроса
        :return bool: True, если вопрос существует, False в противном случае
        """
        query = db.query(exists().where(self.model.question_id == question_id))
        return db.scalar(query)

    def get_last_question(self, db: Session) -> Question | None:
        """
        Возвращает последний добавленный в БД вопрос.

        :param db: Сессия базы данных
        :return Question: Последний сохраненный вопрос, если вопрос существует, None в противном случае
        """
        return db.query(self.model).order_by(self.model.id.desc()).first()

    def bulk_create_questions(self, db: Session, questions: list[QuestionCreate]) -> None:
        """
        Создает вопросы в БД в режиме "bulk create".

        :param db: Сессия базы данных
        :param questions: Список объектов QuestionCreate для создания
        """
        question_objects = [self.model(**q.dict()) for q in questions]
        db.add_all(question_objects)
        db.flush()
        db.commit()


crud_questions = CRUDQuestion(Question)
