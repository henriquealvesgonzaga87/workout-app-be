from fastapi.exceptions import ResponseValidationError

from app.application.user.dtos.user_dtos import UserOutputDto
from app.application.user.interfaces.interfaces import UserInterface
from app.presentation.error_handlers.reponse_error import ResponseError
from app.presentation.error_handlers.type_error import TypeError as CustomTypeError


class GetUserByEmailUseCase:
    def __init__(self, user_repository: UserInterface):
        self.user_repositoy = user_repository

    def prepare(self, email: str) -> str:
        if isinstance(email, str):
            return email
        raise CustomTypeError(f"Expected str got {type(email)} instead")

    def execute(self, email: str) -> UserOutputDto:
        try:
            self.prepare(email=email)
            user = self.user_repositoy.get_by_email(email=email)
            return UserOutputDto(
                id=user.id,
                name=user.name,
                email=user.email,
                password=user.password,
                is_active=user.is_active,
                creation_date=user.creation_date,
                update_date=user.update_date,
            )
        except ResponseValidationError as e:
            raise ResponseError(f"Unable to respond the request! Error: {e}")
