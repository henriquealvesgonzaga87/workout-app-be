import os

from app.application.redis.auth.interfaces.interfaces import RedisAuthRepositoryInterface
from app.presentation.error_handlers.bad_request_error import BadRequestError
from app.presentation.error_handlers.unauthorized_error import UnauthorizedError


class RedisAuthRepository(RedisAuthRepositoryInterface):
    def __init__(self, redis_client):
        self.redis_client = redis_client
        self.REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")

    def revoke_refresh_token(self, refresh_token: str, expires_in: int) -> bool:
        try:
            if not refresh_token:
                raise BadRequestError("Refresh token is required")

            expires_in = int(self.REFRESH_TOKEN_EXPIRE_DAYS) * 24 * 60 * 60  # Default to days in seconds
            if not isinstance(expires_in, int) or expires_in <= 0:
                raise BadRequestError("Expires in must be a positive integer representing seconds")

            revoked_token = self.redis_client.set(refresh_token, "revoked", ex=expires_in)
            return revoked_token
        except Exception as e:
            raise Exception(f"Error revoking refresh token: {str(e)}")

    def is_refresh_token_revoked(self, refresh_token) -> None:
        if not refresh_token:
            raise BadRequestError("Refresh token is required")

        try:
            check_if_token_is_revoked = self.redis_client.get(refresh_token)
            if check_if_token_is_revoked is None:
                return check_if_token_is_revoked
            raise UnauthorizedError("Refresh Token already revoked")
        except Exception as e:
             raise UnauthorizedError(f"Error checking refresh token status: {str(e)}")
