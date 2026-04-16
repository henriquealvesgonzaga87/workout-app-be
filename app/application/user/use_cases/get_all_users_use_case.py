from typing import Any

from pydantic import TypeAdapter, ValidationError

from app.application.auth.jwt.dependencies.verification_dependencies import verify_token_payload_user_role
from app.application.user.dtos.user_dtos import UserOutputDto
from app.application.user.interfaces.interfaces import UserInterface
from app.presentation.error_handlers.reponse_error import ResponseError


class GetAllUsersUseCase:
    def __init__(self, user_repository: UserInterface):
        self.user_repository = user_repository

    def prepare(self,  access_token_payload: dict[str, Any]) -> None:
        verify_token_payload_user_role(access_token_payload=access_token_payload)

    def execute(self,  access_token_payload: dict[str, Any]) -> list[UserOutputDto]:
        self.prepare(access_token_payload=access_token_payload)
        try:
            users = self.user_repository.get_users()
            return TypeAdapter(list[UserOutputDto]).validate_python(users)
        except ValidationError as e:
            raise ResponseError(f"Unable to respond the request! Error: {e}")
