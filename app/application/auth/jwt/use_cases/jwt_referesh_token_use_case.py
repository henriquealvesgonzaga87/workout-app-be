from app.infrastructure.auth.jwt.jwt_handler import JwtHandler
from app.presentation.error_handlers.type_error import TypeError as CustomTypeError
from app.presentation.models.auth.jwt.jwt_models import JwtTokenSchemaResponse


class JwtRefreshTokenUseCases:
    def __init__(self, jwt_handler: JwtHandler):
         self.jwt_handler = jwt_handler

    def prepare(self, refresh_token: str) -> str:
        if not isinstance(refresh_token, str):
              raise CustomTypeError("refresh token must be a str")

        return refresh_token

    def execute(self, refresh_token: str) -> JwtTokenSchemaResponse:
         self.prepare(refresh_token=refresh_token)
         refreshed_token = self.jwt_handler.refresh_token(refresh_token=refresh_token)

         return JwtTokenSchemaResponse(
              access_token=refreshed_token.access_token,
              refresh_token=refreshed_token.refresh_token
         )
