from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ...config.config import settings

engine = create_engine(
    settings.DATABASE_DSN,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
