import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from jose import ExpiredSignatureError, JWTError, jwt

from app.application.auth.jwt.dtos.jwt_dtos import JwtLoginDto, JwtTokenSchemaOutputDto
from app.application.redis.auth.interfaces.interfaces import RedisAuthRepositoryInterface
from app.application.user.interfaces.interfaces import UserInterface
from app.presentation.error_handlers.bad_request_error import BadRequestError
from app.presentation.error_handlers.unauthorized_error import UnauthorizedError

load_dotenv()


class JwtHandler:
    def __init__(self, user_repository: UserInterface, redis_auth_respository: RedisAuthRepositoryInterface):
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
        self.REFRESH_TOKEN_EXPIRE_DAYS = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")
        self.user_repository = user_repository
        self.redis_auth_respository = redis_auth_respository


    def _create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=int(self.ACCESS_TOKEN_EXPIRE_MINUTES)))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)

    def _create_refresh_token(self, data: dict):
        expire = datetime.utcnow() + timedelta(days=int(self.REFRESH_TOKEN_EXPIRE_DAYS))
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.REFRESH_SECRET_KEY, algorithm=self.ALGORITHM)

    def login(self, login_data: JwtLoginDto):
        user = self.user_repository.get_by_email(email=login_data.email)

        access_token = self._create_access_token({
            "id": user.id, 
            "role": user.is_super_admin,
            "is_active": user.is_active,
        })
        refresh_token = self._create_refresh_token({
            "id": user.id, 
            "role": user.is_super_admin,
            "is_active": user.is_active,
        })
        return JwtTokenSchemaOutputDto(
            access_token=access_token, 
            refresh_token=refresh_token
        )

    def refresh_token(self, refresh_token: str):
        if not refresh_token:
            raise BadRequestError("Refresh token is required")

        # if self.is_refresh_token_revoked(refresh_token):
        #     raise UnauthorizedError("Refresh token has been revoked")

        try:
            payload = jwt.decode(refresh_token, self.REFRESH_SECRET_KEY, algorithms=self.ALGORITHM)
            id = payload.get("id")
            role = payload.get("role")
            access_token = self._create_access_token({"id": id, "role": role})
            new_refresh_token = self._create_refresh_token({"id": id, "role": role})
            return JwtTokenSchemaOutputDto(access_token=access_token, refresh_token=new_refresh_token)

        except ExpiredSignatureError:
            raise UnauthorizedError("Invalid refresh token")

        except JWTError:
            raise UnauthorizedError("Invalid refresh token")
