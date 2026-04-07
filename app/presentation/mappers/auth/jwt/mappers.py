from app.application.auth.jwt.dtos.jwt_dtos import JwtLoginDto, JwtTokenSchemaOutputDto
from app.presentation.models.auth.jwt.jwt_models import JwtLoginRequest, JwtTokenSchemaResponse


class JwtMapper:
    @staticmethod
    def to_application_dto(jwt_request_data: JwtLoginRequest) -> JwtLoginDto:
        return JwtLoginDto(
            email=jwt_request_data.email,
            password=jwt_request_data.password
        )

    @staticmethod
    def to_web_response(jwt_output_dto: JwtTokenSchemaOutputDto) -> JwtTokenSchemaResponse:
        return JwtTokenSchemaResponse(
            access_token=jwt_output_dto.access_token,
            refresh_token=jwt_output_dto.refresh_token,
            token_type=jwt_output_dto.token_type
        )
