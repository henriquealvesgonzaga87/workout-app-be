from typing import Any

from fastapi.exceptions import ResponseValidationError

from app.application.auth.jwt.dependencies.verification_dependencies import verify_token_payload_user_role
from app.application.user.interfaces.interfaces import UserInterface
from app.presentation.error_handlers.forbidden_error import ForbiddenError
from app.presentation.error_handlers.reponse_error import ResponseError
from app.presentation.error_handlers.request_error import RequestError


class DeleteUserUseCase:
    def __init__(self, user_repository: UserInterface):
        self.user_repository = user_repository

    def prepare(self, id: int, access_token_payload: dict[str, Any]) -> int:
        try:
            if not isinstance(id, int):
                id = int(id)

            verify_token_payload_user_role(access_token_payload=access_token_payload)

            return id
        except (TypeError, ValueError):
            raise RequestError(f"Expecting int and got {type(id)} instead")
        except ForbiddenError as e:
            raise ForbiddenError(f"{str(e)}")

    def execute(self, id: int, access_token_payload: dict[str, Any]) -> bool:
        try:
            self.prepare(id=id, access_token_payload=access_token_payload)
            self.user_repository.delete(id=id)

            return True

        except ResponseValidationError as e:
            raise ResponseError(f"Unable to respond the request! Error: {e}")
