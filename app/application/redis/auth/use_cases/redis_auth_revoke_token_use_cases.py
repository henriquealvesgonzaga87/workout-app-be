from app.application.redis.auth.interfaces.interfaces import RedisAuthRepositoryInterface
from app.presentation.error_handlers.type_error import TypeError as CustomTyperError
from app.presentation.error_handlers.unauthorized_error import UnauthorizedError


class RedisAuthRevokeTokenUseCase:
    def __init__(self, redis_auth_respository: RedisAuthRepositoryInterface):
        self.redis_auth_respository = redis_auth_respository

    def prepare(self, refresh_token: str, expires_in: int):
        if not isinstance(refresh_token, str):
            raise CustomTyperError("refresh token must be a string")

        if not isinstance(expires_in, int):
            raise CustomTyperError("Expires in must be a valid integer")

        revoked_token = self.redis_auth_respository.is_refresh_token_revoked(refresh_token=refresh_token)
        if revoked_token:
            raise UnauthorizedError("Token already revoked")

    def execute(self, refresh_token: str, expires_in: int) -> bool:
        self.prepare(refresh_token=refresh_token, expires_in=expires_in)

        revoked_token = self.redis_auth_respository.revoke_refresh_token(
            refresh_token=refresh_token,
            expires_in=expires_in
        )

        return revoked_token
