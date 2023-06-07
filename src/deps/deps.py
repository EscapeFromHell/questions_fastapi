from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.clients import QuestionClient
from src.core.db.session import SessionLocal
from src.core.repository import QuestionRepo


def get_db() -> Generator:
    """Генератор сессии БД."""
    with SessionLocal() as db:
        yield db


def question_repo(db: Session = Depends(get_db, use_cache=True)) -> QuestionRepo:
    """DI для репозитория QuestionRepo."""
    return QuestionRepo(db)


def question_client() -> QuestionClient:
    """DI для клиента Question."""
    return QuestionClient()
