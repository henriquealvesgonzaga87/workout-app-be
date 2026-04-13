"""Tests for JWT Handler."""

import os
from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time
from jose import JWTError, jwt

from app.application.auth.jwt.dtos.jwt_dtos import JwtTokenSchemaOutputDto
from app.infrastructure.auth.jwt.jwt_handler import JwtHandler
from app.presentation.error_handlers.unauthorized_error import UnauthorizedError


class TestJwtHandlerInitialization:
    """Test JWT Handler initialization."""

    def test_handler_initialization(self, mock_user_repository, mock_redis_auth_repository):
        """Test JWT handler initializes with correct environment variables."""
        os.environ["SECRET_KEY"] = "test-secret-key-32-chars-minimum9"
        os.environ["REFRESH_SECRET_KEY"] = "test-refresh-key-32-chars-minimum9"
        os.environ["ALGORITHM"] = "HS256"
        os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
        os.environ["REFRESH_TOKEN_EXPIRE_DAYS"] = "7"

        handler = JwtHandler(
            user_repository=mock_user_repository,
            redis_auth_respository=mock_redis_auth_repository
        )

        assert handler.SECRET_KEY == "test-secret-key-32-chars-minimum9"
        assert handler.REFRESH_SECRET_KEY == "test-refresh-key-32-chars-minimum9"
        assert handler.ALGORITHM == "HS256"
        assert handler.ACCESS_TOKEN_EXPIRE_MINUTES == "30"
        assert handler.REFRESH_TOKEN_EXPIRE_DAYS == "7"

    def test_handler_stores_repositories(self, mock_user_repository, mock_redis_auth_repository):
        """Test JWT handler stores repositories."""
        handler = JwtHandler(
            user_repository=mock_user_repository,
            redis_auth_respository=mock_redis_auth_repository
        )

        assert handler.user_repository == mock_user_repository
        assert handler.redis_auth_respository == mock_redis_auth_repository


class TestJwtHandlerCreateAccessToken:
    """Test JWT Handler create_access_token method."""

    def test_create_access_token_returns_string(self, jwt_handler):
        """Test create_access_token returns a string."""
        token = jwt_handler._create_access_token(data={"id": 1, "role": False})

        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_is_valid_jwt(self, jwt_handler):
        """Test created access token is valid JWT."""
        token = jwt_handler._create_access_token(data={"id": 1, "role": False})

        decoded = jwt.decode(
            token,
            jwt_handler.SECRET_KEY,
            algorithms=jwt_handler.ALGORITHM
        )

        assert decoded["id"] == 1
        assert decoded["role"] is False

    def test_create_access_token_includes_exp_claim(self, jwt_handler):
        """Test access token includes expiration claim."""
        token = jwt_handler._create_access_token(data={"id": 1, "role": False})

        decoded = jwt.decode(
            token,
            jwt_handler.SECRET_KEY,
            algorithms=jwt_handler.ALGORITHM
        )

        assert "exp" in decoded

    def test_create_access_token_with_custom_expiry(self, jwt_handler):
        """Test create_access_token with custom expiry time."""
        custom_delta = timedelta(minutes=60)
        token = jwt_handler._create_access_token(
            data={"id": 1, "role": False},
            expires_delta=custom_delta
        )

        decoded = jwt.decode(
            token,
            jwt_handler.SECRET_KEY,
            algorithms=jwt_handler.ALGORITHM
        )

        assert decoded["id"] == 1
        assert "exp" in decoded

    def test_create_access_token_respects_expiry_delta(self, jwt_handler):
        """Test access token respects custom expiry delta."""
        with freeze_time("2026-04-13 12:00:00"):
            custom_delta = timedelta(minutes=10)
            token = jwt_handler._create_access_token(
                data={"id": 1, "role": False},
                expires_delta=custom_delta
            )

            decoded = jwt.decode(
                token,
                jwt_handler.SECRET_KEY,
                algorithms=jwt_handler.ALGORITHM
            )

            # Expiry should be approximately 10 minutes from now
            exp_time = datetime.utcfromtimestamp(decoded["exp"])
            current_time = datetime.utcnow()
            delta = exp_time - current_time

            assert 9 * 60 < delta.total_seconds() < 11 * 60

    def test_create_access_token_with_admin_role(self, jwt_handler):
        """Test create_access_token preserves admin role."""
        token = jwt_handler._create_access_token(data={"id": 1, "role": True})

        decoded = jwt.decode(
            token,
            jwt_handler.SECRET_KEY,
            algorithms=jwt_handler.ALGORITHM
        )

        assert decoded["role"] is True

    def test_create_access_token_different_for_different_users(self, jwt_handler):
        """Test access tokens are different for different users."""
        token1 = jwt_handler._create_access_token(data={"id": 1, "role": False})
        token2 = jwt_handler._create_access_token(data={"id": 2, "role": False})

        # Tokens should be different
        assert token1 != token2

    def test_create_access_token_default_expiry(self, jwt_handler):
        """Test access token uses default expiry when not specified."""
        with freeze_time("2026-04-13 12:00:00"):
            token = jwt_handler._create_access_token(data={"id": 1, "role": False})

            decoded = jwt.decode(
                token,
                jwt_handler.SECRET_KEY,
                algorithms=jwt_handler.ALGORITHM
            )

            exp_time = datetime.utcfromtimestamp(decoded["exp"])
            current_time = datetime.utcnow()
            delta = exp_time - current_time

            # Should be approximately 30 minutes (default)
            assert 29 * 60 < delta.total_seconds() < 31 * 60


class TestJwtHandlerCreateRefreshToken:
    """Test JWT Handler create_refresh_token method."""

    def test_create_refresh_token_returns_string(self, jwt_handler):
        """Test create_refresh_token returns a string."""
        token = jwt_handler._create_refresh_token(data={"id": 1, "role": False})

        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_refresh_token_is_valid_jwt(self, jwt_handler):
        """Test created refresh token is valid JWT."""
        token = jwt_handler._create_refresh_token(data={"id": 1, "role": False})

        decoded = jwt.decode(
            token,
            jwt_handler.REFRESH_SECRET_KEY,
            algorithms=jwt_handler.ALGORITHM
        )

        assert decoded["id"] == 1
        assert decoded["role"] is False

    def test_create_refresh_token_includes_exp_claim(self, jwt_handler):
        """Test refresh token includes expiration claim."""
        token = jwt_handler._create_refresh_token(data={"id": 1, "role": False})

        decoded = jwt.decode(
            token,
            jwt_handler.REFRESH_SECRET_KEY,
            algorithms=jwt_handler.ALGORITHM
        )

        assert "exp" in decoded

    def test_create_refresh_token_uses_refresh_secret(self, jwt_handler):
        """Test refresh token uses refresh secret key."""
        token = jwt_handler._create_refresh_token(data={"id": 1, "role": False})

        # Should decode with refresh secret
        decoded = jwt.decode(
            token,
            jwt_handler.REFRESH_SECRET_KEY,
            algorithms=jwt_handler.ALGORITHM
        )

        assert decoded is not None

        # Should NOT decode with access secret
        with pytest.raises(JWTError):
            jwt.decode(
                token,
                jwt_handler.SECRET_KEY,
                algorithms=jwt_handler.ALGORITHM
            )

    def test_create_refresh_token_expiry(self, jwt_handler):
        """Test refresh token expiry is set to days."""
        with freeze_time("2026-04-13 12:00:00"):
            token = jwt_handler._create_refresh_token(data={"id": 1, "role": False})

            decoded = jwt.decode(
                token,
                jwt_handler.REFRESH_SECRET_KEY,
                algorithms=jwt_handler.ALGORITHM
            )

            exp_time = datetime.utcfromtimestamp(decoded["exp"])
            current_time = datetime.utcnow()
            delta = exp_time - current_time

            # Should be approximately 7 days (default)
            assert 6.9 * 24 * 60 * 60 < delta.total_seconds() < 7.1 * 24 * 60 * 60

    def test_create_refresh_token_different_for_different_users(self, jwt_handler):
        """Test refresh tokens are different for different users."""
        token1 = jwt_handler._create_refresh_token(data={"id": 1, "role": False})
        token2 = jwt_handler._create_refresh_token(data={"id": 2, "role": False})

        assert token1 != token2


class TestJwtHandlerLogin:
    """Test JWT Handler login method."""

    def test_login_returns_token_schema_output_dto(
        self,
        jwt_handler,
        mock_jwt_login_dto,
        mock_user_repository,
        mock_user_entity
    ):
        """Test login method returns JwtTokenSchemaOutputDto."""
        mock_user_repository.get_by_email.return_value = mock_user_entity

        result = jwt_handler.login(login_data=mock_jwt_login_dto)

        assert isinstance(result, JwtTokenSchemaOutputDto)

    def test_login_returns_access_and_refresh_tokens(
        self,
        jwt_handler,
        mock_jwt_login_dto,
        mock_user_repository,
        mock_user_entity
    ):
        """Test login method returns both access and refresh tokens."""
        mock_user_repository.get_by_email.return_value = mock_user_entity

        result = jwt_handler.login(login_data=mock_jwt_login_dto)

        assert result.access_token is not None
        assert result.refresh_token is not None
        assert result.token_type == "bearer"

    def test_login_tokens_are_valid(
        self,
        jwt_handler,
        mock_jwt_login_dto,
        mock_user_repository,
        mock_user_entity
    ):
        """Test login returns valid tokens."""
        mock_user_repository.get_by_email.return_value = mock_user_entity

        result = jwt_handler.login(login_data=mock_jwt_login_dto)

        # Verify access token
        access_decoded = jwt.decode(
            result.access_token,
            jwt_handler.SECRET_KEY,
            algorithms=jwt_handler.ALGORITHM
        )
        assert access_decoded["id"] == mock_user_entity.id

        # Verify refresh token
        refresh_decoded = jwt.decode(
            result.refresh_token,
            jwt_handler.REFRESH_SECRET_KEY,
            algorithms=jwt_handler.ALGORITHM
        )
        assert refresh_decoded["id"] == mock_user_entity.id

    def test_login_creates_tokens_with_user_role(
        self,
        jwt_handler,
        mock_jwt_login_dto,
        mock_user_repository,
        mock_super_admin_entity
    ):
        """Test login creates tokens with correct role."""
        mock_jwt_login_dto.email = "admin@example.com"
        mock_user_repository.get_by_email.return_value = mock_super_admin_entity

        result = jwt_handler.login(login_data=mock_jwt_login_dto)

        access_decoded = jwt.decode(
            result.access_token,
            jwt_handler.SECRET_KEY,
            algorithms=jwt_handler.ALGORITHM
        )
        assert access_decoded["role"] is True


class TestJwtHandlerRefreshToken:
    """Test JWT Handler refresh_token method."""

    def test_refresh_token_returns_token_schema_output_dto(
        self,
        jwt_handler,
        valid_refresh_token,
        mock_user_entity
    ):
        """Test refresh_token method returns JwtTokenSchemaOutputDto."""
        result = jwt_handler.refresh_token(refresh_token=valid_refresh_token)

        assert isinstance(result, JwtTokenSchemaOutputDto)

    def test_refresh_token_returns_new_access_token(
        self,
        jwt_handler,
        valid_refresh_token,
        mock_user_entity
    ):
        """Test refresh_token method returns new access token."""
        result = jwt_handler.refresh_token(refresh_token=valid_refresh_token)

        assert result.access_token is not None
        assert result.access_token != valid_refresh_token

    def test_refresh_token_returns_new_refresh_token(
        self,
        jwt_handler,
        valid_refresh_token,
        mock_user_entity
    ):
        """Test refresh_token method returns new refresh token."""
        result = jwt_handler.refresh_token(refresh_token=valid_refresh_token)

        assert result.refresh_token is not None

    def test_refresh_token_with_valid_token(
        self,
        jwt_handler,
        valid_refresh_token
    ):
        """Test refresh_token successfully handles valid token."""
        result = jwt_handler.refresh_token(refresh_token=valid_refresh_token)

        assert result is not None
        assert hasattr(result, 'access_token')
        assert hasattr(result, 'refresh_token')

    def test_refresh_token_validates_signature(
        self,
        jwt_handler,
        mock_user_entity
    ):
        """Test refresh_token validates token signature."""
        # Create token with wrong secret
        invalid_token = jwt.encode(
            {"id": mock_user_entity.id, "role": False},
            "wrong-secret",
            algorithm=jwt_handler.ALGORITHM
        )

        with pytest.raises(UnauthorizedError):
            jwt_handler.refresh_token(refresh_token=invalid_token)

    def test_refresh_token_preserves_user_id(
        self,
        jwt_handler,
        valid_refresh_token,
        mock_user_entity
    ):
        """Test refresh_token preserves user id."""
        result = jwt_handler.refresh_token(refresh_token=valid_refresh_token)

        access_decoded = jwt.decode(
            result.access_token,
            jwt_handler.SECRET_KEY,
            algorithms=jwt_handler.ALGORITHM
        )

        assert access_decoded["id"] == mock_user_entity.id

    def test_refresh_token_preserves_user_role(
        self,
        jwt_handler,
        valid_refresh_token,
        mock_user_entity
    ):
        """Test refresh_token preserves user role."""
        result = jwt_handler.refresh_token(refresh_token=valid_refresh_token)

        access_decoded = jwt.decode(
            result.access_token,
            jwt_handler.SECRET_KEY,
            algorithms=jwt_handler.ALGORITHM
        )

        assert access_decoded["role"] == mock_user_entity.is_super_admin
