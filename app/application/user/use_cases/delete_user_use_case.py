from fastapi.exceptions import ResponseValidationError

from app.application.user.interfaces.interfaces import UserInterface
from app.presentation.error_handlers.reponse_error import ResponseError
from app.presentation.error_handlers.request_error import RequestError


class DeleteUserUseCase:
    def __init__(self, user_repository: UserInterface):
        self.user_repository = user_repository

    def prepare(self, id: int) -> int:
        try:
            if isinstance(id, int):
                return id
            if not isinstance(id, int):
                id = int(id)
                return id
        except Exception:
            raise RequestError(f"Expecting int and got {type(id)} instead")

    def execute(self, id: int) -> bool:
        try:
            self.prepare(id=id)
            self.user_repository.delete(id=id)

            return True

        except ResponseValidationError as e:
            raise ResponseError(f"Unable to respond the request! Error: {e}")
