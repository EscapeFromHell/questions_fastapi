import logging

import httpx
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from src.config import settings
from src.core.schemas import QuestionCreate
from src.utils import get_logger

logger = get_logger(__file__, logging.DEBUG)


class QuestionClient:
    async def get_questions(self, questions_num: int) -> list[QuestionCreate]:
        """
        Получение вопросов для викторины.

        :param questions_num: Количество вопросов
        :return list[QuestionCreate]: Список вопросов
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url=settings.QUESTION_URL,
                    params={"count": questions_num},
                    headers={"Content-Type": "application/json"},
                )

        except (httpx.ConnectError, httpx.ConnectTimeout) as error:
            logger.error(f"Ошибка при обращении к API: {error}")
            raise HTTPException(status_code=response.status_code, detail=f"Ошибка при обращении к API: {error}")

        else:
            if response.is_error:
                logger.error(f"Ошибка при обращении к API: {response.content}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Ошибка при обращении к API: {response.content}",
                )
            data = jsonable_encoder(response.json())
            questions = []

            for question in data:
                questions.append(
                    QuestionCreate(
                        question_id=question["id"],
                        question=question["question"],
                        answer=question["answer"],
                        created_at=question["created_at"],
                    )
                )
            return questions
