from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError
from sqlalchemy.orm import Session

from app.application.user.interfaces.interfaces import UserInterface
from app.domain.user.entities import User
from app.infrastructure.schemas.user.user_schema import UserSchema
from app.presentation.error_handlers.integrity_error import IntegrityError


class SQLAlchemyUserRepository(UserInterface):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, user: User) -> User:
        try:
            new_user = UserSchema(
                name = user.name,
                email = user.email,
                password = user.password,
                is_active = user.is_active,
                is_super_admin = user.is_super_admin,
                creation_date = user.creation_date,
                update_date = None
            )
            self.db_session.add(new_user)
            self.db_session.commit()
            self.db_session.refresh(new_user)
            return User(
                id = new_user.id,
                name = new_user.name,
                email = new_user.email,
                password = new_user.password,
                is_active = new_user.is_active,
                is_super_admin = new_user.is_super_admin,
                creation_date = new_user.creation_date,
                update_date = new_user.update_date
            )
        except SQLAlchemyIntegrityError as e:
            self.db_session.rollback()
            raise IntegrityError(f"Error to save into DB! Error: {e}")
        finally:
            self.db_session.close()
