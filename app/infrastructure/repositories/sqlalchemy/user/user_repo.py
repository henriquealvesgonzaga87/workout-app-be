from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.application.user.interfaces.interfaces import UserInterface
from app.domain.user.entities import User
from app.infrastructure.schemas.user.user_schema import UserSchema
from app.presentation.error_handlers.atribute_error import AttributeError as CustomAttributeError
from app.presentation.error_handlers.data_base_error import DataBaseError
from app.presentation.error_handlers.integrity_error import IntegrityError
from app.presentation.error_handlers.not_found_error import NotFoundError


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

    def get_users(self) -> list[User]:
        try:
            users = self.db_session.query(UserSchema).all()

            if len(users) == 0:
                raise NotFoundError("No result found")

            return users
        except SQLAlchemyError as e:
            raise DataBaseError(f"Impossible to proccess right now! Error: {e}")

    def get_by_id(self, id: int) -> User:
        try:
            user = self.db_session.query(UserSchema).filter(UserSchema.id==id).first()

            if user is None:
                raise NotFoundError(f"User with ID {id} not found")

            return user
        except SQLAlchemyError as e:
            raise DataBaseError(f"Impossible to proccess right now! Error: {e}")

    def get_by_email(self, email: str) -> User:
        try:
            user = self.db_session.query(UserSchema).filter(UserSchema.email==email).first()

            if user is None:
                raise NotFoundError(f"User with email {email} not found")

            return user
        except SQLAlchemyError as e:
            raise DataBaseError(f"Impossible to proccess right now! Error: {e}")

    def update(self, id: int, user: User) -> User:
        try:
            db_user = self.db_session.query(UserSchema).filter(UserSchema.id == id).first()

            if db_user is None:
                raise NotFoundError(f"User with id {id} not found")

            update_data = user.model_dump(exclude_unset=True, exclude_none=True)

            for key, value in update_data.items():
                setattr(db_user, key, value)

            self.db_session.commit()
            self.db_session.refresh(db_user)

            return User(
                id = db_user.id,
                name = db_user.name,
                email = db_user.email,
                password = db_user.password,
                is_active = db_user.is_active,
                is_super_admin = db_user.is_super_admin,
                creation_date = db_user.creation_date,
                update_date = db_user.update_date
            )

        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise DataBaseError(f"Impossible to proccess right now! Error: {e}")
        except AttributeError as e:
            self.db_session.rollback()
            raise CustomAttributeError(f"Impossible to proccess due to db issues: {e}")

    def delete(self, id: int) -> bool:
        try:
            query_user = self.get_by_id(id=id)

            self.db_session.delete(query_user)
            self.db_session.commit()

            return True
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise DataBaseError(f"Impossible to proccess right now! Error: {e}")
        except AttributeError as e:
            self.db_session.rollback()
            raise CustomAttributeError(f"Impossible to proccess due to db issues: {e}")
