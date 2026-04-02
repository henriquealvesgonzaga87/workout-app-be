from pydantic_core import ValidationError

from app.application.user.dtos.user_dtos import CreateUserDto, UserOutputDto
from app.application.user.interfaces.interfaces import UserInterface
from app.presentation.error_handlers.reponse_error import ResponseError
from app.presentation.error_handlers.request_error import RequestError
from utils.hash import get_password_hash


class CreateUserUseCase:
    def __init__(self, user_repository: UserInterface):
        self.user_repository = user_repository

    def prepare(self, user_dto: CreateUserDto) -> CreateUserDto:
        try:
            hashed_password = get_password_hash(user_dto.password)
            return CreateUserDto(
                name=user_dto.name,
                email=user_dto.email,
                password=hashed_password,
                is_active=user_dto.is_active,
                is_super_admin=user_dto.is_super_admin,
                creation_date=user_dto.creation_date,
                update_date=user_dto.update_date,
            )
        except ValidationError as e:
            raise RequestError(f"Error while processing the request! Bad Request! Error: {e}")

    def execute(self, user_dto: CreateUserDto) -> UserOutputDto:
        try:
            user_data = self.prepare(user_dto=user_dto)
            new_user = self.user_repository.create(user=user_data)
            return UserOutputDto(
                id=new_user.id,
                name=new_user.name,
                email=new_user.email,
                password=new_user.password,
                is_active=new_user.is_active,
            )
        except ValidationError as e:
            raise ResponseError(f"Error to respond the request, but the data was saved on DB! Error: {e}")
