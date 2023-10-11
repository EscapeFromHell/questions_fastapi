from fastapi import APIRouter, Depends, Query

from src.core.clients import QuestionClient
from src.core.repository import QuestionRepo
from src.core.schemas import Question, QuestionEmpty
from src.deps import question_client as deps_question_client
from src.deps import question_repo as deps_question_repo

router = APIRouter()


@router.post("/", status_code=200, response_model=Question | QuestionEmpty)
async def get_questions(
    *,
    questions_num: int = Query(ge=1, le=1000),
    question_repo: QuestionRepo = Depends(deps_question_repo),
    question_client: QuestionClient = Depends(deps_question_client)
) -> Question | QuestionEmpty:
    """
    Получение вопросов для викторины.

    :param questions_num: Количество вопросов (от 1 до 1000)
    :param question_repo: QuestionRepo
    :param question_client: QuestionClient
    :return Question: Последний добавленный в БД вопрос или пустой объект Question (если БД пуста)
    """
    return await question_repo.get_questions(questions_num, question_client)
