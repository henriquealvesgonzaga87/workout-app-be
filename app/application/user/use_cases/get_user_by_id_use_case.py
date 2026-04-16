from typing import Any

from fastapi.exceptions import ResponseValidationError

from app.application.auth.jwt.dependencies.verification_dependencies import verify_token_payload_user_id
from app.application.user.dtos.user_dtos import UserOutputDto
from app.application.user.interfaces.interfaces import UserInterface
from app.presentation.error_handlers.forbidden_error import ForbiddenError
from app.presentation.error_handlers.reponse_error import ResponseError
from app.presentation.error_handlers.request_error import RequestError


class GetUserByIdUseCase:
    def __init__(self, user_repository: UserInterface):
        self.user_repositoy = user_repository

    def prepare(self, id: int, access_token_payload: dict[str, Any]) -> None:
        try:
            if not isinstance(id, int):
                id = int(id)

            verify_token_payload_user_id(id=id, access_token_payload=access_token_payload)

        except (TypeError, ValueError):
            raise RequestError(f"Expecting int and got {type(id)} instead")
        except ForbiddenError as e:
            raise ForbiddenError(f"{str(e)}")

    def execute(self, id: int, access_token_payload: dict[str, Any]) -> UserOutputDto:
        try:
            self.prepare(id=id, access_token_payload=access_token_payload)
            user = self.user_repositoy.get_by_id(id=id)
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
