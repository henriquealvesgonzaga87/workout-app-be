from app.application.auth.jwt.dtos.jwt_dtos import JwtLoginDto
from app.application.user.interfaces.interfaces import UserInterface
from app.domain.user.entities import User
from app.infrastructure.auth.jwt.jwt_handler import JwtHandler
from app.infrastructure.auth.jwt.password_hasher import verify_password
from app.presentation.error_handlers.not_found_error import NotFoundError
from app.presentation.error_handlers.unauthorized_error import UnauthorizedError
from app.presentation.models.auth.jwt.jwt_models import JwtTokenSchemaResponse


class JwtLoginUseCases:
    def __init__(self, jwt_handler: JwtHandler, user_repository: UserInterface):
        self.jwt_handler = jwt_handler
        self.user_repository = user_repository

    def prepare(self, login_data: JwtLoginDto) -> User:
        user = self.user_repository.get_by_email(email=login_data.email)

        if user.is_active is False:
            raise NotFoundError("User not registered. Please register and then login")

        check_credentials = verify_password(plain_password=login_data.password, hashed_password=user.password)

        if check_credentials is False:
            raise UnauthorizedError("Incorrect email or password")

        return user

    def execute(self, login_data: JwtLoginDto) -> JwtTokenSchemaResponse:
        self.prepare(login_data=login_data)
        authentica_user = self.jwt_handler.login(login_data=login_data)

        return JwtTokenSchemaResponse(
            access_token=authentica_user.access_token,
            refresh_token=authentica_user.refresh_token
        )
