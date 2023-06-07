from fastapi import APIRouter, Depends
from pydantic import PositiveInt

from src.core.clients import QuestionClient
from src.core.repository import QuestionRepo
from src.core.schemas import Question
from src.deps import question_client as deps_question_client
from src.deps import question_repo as deps_question_repo

router = APIRouter()


@router.post("/", status_code=200, response_model=Question | None)
async def get_questions(
    *,
    questions_num: PositiveInt,
    question_repo: QuestionRepo = Depends(deps_question_repo),
    question_client: QuestionClient = Depends(deps_question_client)
) -> Question | None:
    """
    Получение вопросов для викторины.

    :param questions_num: Количество вопросов
    :param question_repo: QuestionRepo
    :param question_client: QuestionClient
    :return Question: Последний добавленный в БД вопрос или None (если БД пуста)
    """
    return await question_repo.get_questions(questions_num, question_client)
