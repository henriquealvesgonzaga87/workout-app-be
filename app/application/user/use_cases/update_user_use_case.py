from typing import Any

from pydantic_core import ValidationError

from app.application.auth.jwt.dependencies.verification_dependencies import verify_token_payload_user_id
from app.application.user.dtos.user_dtos import UpdateUserDto, UserOutputDto
from app.application.user.interfaces.interfaces import UserInterface
from app.infrastructure.auth.jwt.password_hasher import get_password_hash
from app.presentation.error_handlers.forbidden_error import ForbiddenError
from app.presentation.error_handlers.reponse_error import ResponseError
from app.presentation.error_handlers.request_error import RequestError


class UpdateUserUseCase:
    def __init__(self, user_repository: UserInterface):
        self.user_repository = user_repository

    def prepare(self, id: int, user_dto: UpdateUserDto, access_token_payload: dict[str, Any]) -> UpdateUserDto:
        try:
            verify_token_payload_user_id(id=id, access_token_payload=access_token_payload)

            return UpdateUserDto(
                name=user_dto.name,
                email=user_dto.email,
                password=user_dto.password if user_dto.password is None else get_password_hash(user_dto.password),
                is_active=user_dto.is_active,
                is_super_admin=user_dto.is_super_admin,
                creation_date=user_dto.creation_date,
                update_date=user_dto.update_date,
            )
        except ValidationError as e:
            raise RequestError(f"Error while processing the request! Bad Request! Error: {e}")
        except ForbiddenError as e:
            raise ForbiddenError(f"{str(e)}")

    def execute(self, id: int, user_dto: UpdateUserDto, access_token_payload: dict[str, Any]) -> UserOutputDto:
        try:
            user_data = self.prepare(
                id=id,
                user_dto=user_dto,
                access_token_payload=access_token_payload    
            )
            updated_user = self.user_repository.update(
                id=id,
                user=user_data,
            )
            return UserOutputDto(
                id=updated_user.id,
                name=updated_user.name,
                email=updated_user.email,
                password=updated_user.password,
                is_active=updated_user.is_active,
                creation_date=updated_user.creation_date,
                update_date=updated_user.update_date,
            )
        except ValidationError as e:
            raise ResponseError(f"Error to respond the request, but the data was saved on DB! Error: {e}")
