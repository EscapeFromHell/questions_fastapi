import logging

from pydantic import ValidationError

from src.core.clients import QuestionClient
from src.core.crud import crud_questions
from src.core.repository.repository import Repository
from src.core.schemas import Question, QuestionCreate, QuestionEmpty
from src.utils import get_logger

MAX_RETRIES = 10

logger = get_logger(__file__, logging.DEBUG)


class QuestionRepo(Repository):
    def _get_last_question(self) -> Question | QuestionEmpty:
        """
        Функция для получения последнего сохраненного вопроса в БД.

        :return Question | QuestionEmpty: Последний сохраненный вопрос, если вопрос существует,
        QuestionEmpty в противном случае
        """
        last_question = crud_questions.get_last_question(db=self.db)
        if not last_question:
            last_question = QuestionEmpty(
                id=None,
                question_id=None,
                question=None,
                answer=None,
                created_at=None,
            )
        return last_question

    def _add_questions_to_db(self, questions: list[QuestionCreate]) -> None:
        """
        Функция для записи вопросов в БД.

        :param questions: list[QuestionCreate]
        :return Question: Вопрос в БД с id
        """
        crud_questions.bulk_create_questions(db=self.db, questions=questions)

    def _check_questions_in_db(self, questions: list[QuestionCreate]) -> list[QuestionCreate]:
        """
        Функция для проверки вопросов на наличие в БД.

        :param questions: Список вопросов
        :return list[QuestionCreate]: Список уникальных вопросов
        """
        question_ids = [question.question_id for question in questions]
        question_ids_in_db = []

        for question_id in question_ids:
            if crud_questions.question_exists(db=self.db, question_id=question_id):
                logger.info(f"Question with question_id: {question_id} already in database")
                question_ids_in_db.append(question_id)

        return [question for question in questions if question.question_id not in question_ids_in_db]

    def _prepare_data(self, data: list) -> list[QuestionCreate]:
        """
        Функция для валидации полученных по API вопросов.

        :param data: Список вопросов, полученных по API
        :return list[QuestionCreate]: Список вопросов QuestionCreate
        """
        questions = []

        for question in data:
            try:
                questions.append(
                    QuestionCreate(
                        question_id=question.get("id"),
                        question=question.get("question"),
                        answer=question.get("answer"),
                        created_at=question.get("created_at"),
                    )
                )
            except ValidationError as e:
                logger.error(f"Validation error: {e}")

        return questions

    async def get_questions(self, questions_num: int, question_client: QuestionClient) -> Question | QuestionEmpty:
        """
        Функция получает вопросы через question client и возвращает последний сохраненный вопрос из БД.

        :param questions_num: Количество вопросов
        :param question_client: QuestionClient
        :return Question: Последний добавленный в БД вопрос или пустой объект QuestionEmpty (если БД пуста)
        """
        last_question = self._get_last_question()

        questions_counter = 0
        retries = 0
        while questions_counter < questions_num:
            data = await question_client.get_questions(questions_num - questions_counter)
            questions = self._prepare_data(data=data)
            new_questions = self._check_questions_in_db(questions)
            questions_counter += len(new_questions)
            self._add_questions_to_db(questions=new_questions)
            retries += 1
            if retries == MAX_RETRIES:
                logger.error(
                    f"Failed to find {questions_num - questions_counter} new questions after {MAX_RETRIES} retries."
                )
                break

        return last_question
