from typing import Generator

from sqlalchemy.orm import Session

from app.infrastructure.db.sqlite.database import ScopedSession


def get_db() -> Generator[Session, None, None]:
    session = ScopedSession()
    try:
        yield session
    finally:
        session.close()
        ScopedSession.remove()
