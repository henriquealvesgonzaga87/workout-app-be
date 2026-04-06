from datetime import datetime

from pydantic import TypeAdapter

from app.application.user.dtos.user_dtos import CreateUserDto, UpdateUserDto, UserOutputDto
from app.presentation.models.user.create_user_model import (
    CreateUserRequest,
    CreateUserResponse,
    UpdateUserRequest,
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
    def to_application_dto_update(user_request_data: UpdateUserRequest) -> UpdateUserDto:
        return UpdateUserDto(
            name=user_request_data.name,
            email=user_request_data.email,
            password=user_request_data.password,
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=datetime.utcnow()
        )

    @staticmethod
    def to_web_response(user_output_dto: UserOutputDto) -> CreateUserResponse:
        if isinstance(user_output_dto, UserOutputDto):
            return CreateUserResponse(
                id=user_output_dto.id,
                name=user_output_dto.name,
                email=user_output_dto.email,
                password=user_output_dto.password,
                is_active=user_output_dto.is_active,
                creation_date=user_output_dto.creation_date,
                update_date=user_output_dto.update_date,
            )
        if isinstance(user_output_dto, list):
            return TypeAdapter(list[UserOutputDto]).validate_python(user_output_dto)
