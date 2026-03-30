from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.settings import get_settings


settings = get_settings()

def get_db() -> Generator[Session, None, None]:
    engine = create_engine(settings.DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
    session = sessionmaker()
    db = session(autocommit=False, autoflush=False, bind=engine)
    try:
        yield db
    finally:
        db.close()
