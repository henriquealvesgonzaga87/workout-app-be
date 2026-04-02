from fastapi.exceptions import ResponseValidationError

from app.application.user.dtos.user_dtos import UserOutputDto
from app.application.user.interfaces.interfaces import UserInterface
from app.presentation.error_handlers.reponse_error import ResponseError
from app.presentation.error_handlers.request_error import RequestError


class GetUserByIdUseCase:
    def __init__(self, user_repository: UserInterface):
        self.user_repositoy = user_repository

    def prepare(self, id: int) -> int:
        try:
            if isinstance(id, int):
                return id
            if not isinstance(id, int):
                id = int(id)
                return id
        except Exception:
            raise RequestError(f"Expecting int and got {type(id)} instead")

    def execute(self, id: int) -> UserOutputDto:
        try:
            self.prepare(id=id)
            user = self.user_repositoy.get_by_id(id=id)
            return UserOutputDto(
                id=user.id,
                name=user.name,
                email=user.email,
                password=user.password,
                is_active=user.is_active,
            )
        except ResponseValidationError as e:
            raise ResponseError(f"Unable to respond the request! Error: {e}")
