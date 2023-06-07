from pydantic import PositiveInt

from src.core.clients import QuestionClient
from src.core.crud import crud_questions
from src.core.repository.repository import Repository
from src.core.schemas import Question, QuestionCreate


class QuestionRepo(Repository):
    def __add_question_to_db(self, question: QuestionCreate) -> Question:
        """
        Функция для записи вопроса в БД.

        :param question: QuestionCreate
        :return Question: Вопрос в БД с id
        """
        return crud_questions.create(db=self.db, obj_in=question)

    def __get_unique_questions(self, questions: list[QuestionCreate]) -> list[QuestionCreate]:
        """
        Функция для проверки вопросов на наличие в БД.

        :param questions: Список вопросов
        :return list[QuestionCreate]: Список уникальных вопросов
        """
        question_ids = [question.question_id for question in questions]
        questions_in_db = crud_questions.get_questions(db=self.db, questions_id=question_ids)
        question_ids_in_db = [question.question_id for question in questions_in_db]
        return [question for question in questions if question.question_id not in question_ids_in_db]

    async def get_questions(self, questions_num: PositiveInt, question_client: QuestionClient) -> Question | None:
        """
        Функция для получения вопросов.

        :param questions_num: Количество вопросов
        :param question_client: QuestionClient
        :return Question | None: Последний добавленный в БД вопрос или None (если БД пуста)
        """
        last_question = crud_questions.get_last_question(db=self.db)

        new_questions = []
        while len(new_questions) < questions_num:
            questions = await question_client.get_questions(questions_num - len(new_questions))
            unique_questions = self.__get_unique_questions(questions)
            new_questions.extend(unique_questions)

        for question in new_questions:
            self.__add_question_to_db(question)

        return last_question
