from datetime import datetime

from pydantic import TypeAdapter

from app.application.user.dtos.user_dtos import CreateUserDto, UserOutputDto
from app.presentation.models.user.create_user_model import (
    CreateUserRequest,
    CreateUserResponse,
)


class UserMapper:
    @staticmethod
    def to_application_dto(user_request_data: CreateUserRequest) -> CreateUserDto:
        return CreateUserDto(
            name=user_request_data.name,
            email=user_request_data.email,
            password=user_request_data.password,
            is_active=True,
            is_super_admin=False,
            creation_date=datetime.utcnow(),
            update_date=None
        )

    @staticmethod
    def to_web_response(user_output_dto: UserOutputDto) -> CreateUserResponse:
        if isinstance(user_output_dto, UserOutputDto):
            return CreateUserResponse(
                id=user_output_dto.id,
                name=user_output_dto.name,
                email=user_output_dto.email,
                password=user_output_dto.password,
                is_active=user_output_dto.is_active
            )
        if isinstance(user_output_dto, list):
            return TypeAdapter(list[UserOutputDto]).validate_python(user_output_dto)
