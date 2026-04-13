"""Fixtures and configuration for auth tests."""

import os
from datetime import datetime, timedelta
from unittest.mock import Mock

import pytest
from freezegun import freeze_time

from app.application.auth.jwt.dtos.jwt_dtos import JwtLoginDto, JwtTokenSchemaOutputDto
from app.domain.user.entities import User
from app.infrastructure.auth.jwt.jwt_handler import JwtHandler


# ===== USER ENTITIES =====
@pytest.fixture
def mock_user_entity():
    """Mock user entity for authentication tests."""
    from app.infrastructure.auth.jwt.password_hasher import get_password_hash
    hashed_password = get_password_hash("password123")
    return User(
        id=1,
        name="John Doe",
        email="john@example.com",
        password=hashed_password,
        is_active=True,
        is_super_admin=False,
        creation_date=datetime(2026, 4, 1, 10, 0, 0),
        update_date=None
    )


@pytest.fixture
def mock_super_admin_entity():
    """Mock super admin user entity."""
    from app.infrastructure.auth.jwt.password_hasher import get_password_hash
    hashed_password = get_password_hash("password123")
    return User(
        id=2,
        name="Admin User",
        email="admin@example.com",
        password=hashed_password,
        is_active=True,
        is_super_admin=True,
        creation_date=datetime(2026, 4, 1, 10, 0, 0),
        update_date=None
    )


@pytest.fixture
def mock_inactive_user_entity():
    """Mock inactive user entity."""
    from app.infrastructure.auth.jwt.password_hasher import get_password_hash
    hashed_password = get_password_hash("password123")
    return User(
        id=3,
        name="Inactive User",
        email="inactive@example.com",
        password=hashed_password,
        is_active=False,
        is_super_admin=False,
        creation_date=datetime(2026, 4, 1, 10, 0, 0),
        update_date=None
    )


# ===== DTOs =====
@pytest.fixture
def mock_jwt_login_dto():
    """Mock JWT login DTO."""
    return JwtLoginDto(
        email="john@example.com",
        password="password123"
    )


@pytest.fixture
def mock_jwt_invalid_password_dto():
    """Mock JWT login DTO with invalid password."""
    return JwtLoginDto(
        email="john@example.com",
        password="wrong_password"
    )


@pytest.fixture
def mock_jwt_token_output_dto():
    """Mock JWT token output DTO."""
    return JwtTokenSchemaOutputDto(
        access_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        refresh_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        token_type="bearer"
    )


# ===== MOCKS & REPOSITORIES =====
@pytest.fixture
def mock_user_repository():
    """Mock user repository."""
    return Mock()


@pytest.fixture
def mock_redis_auth_repository():
    """Mock redis auth repository."""
    return Mock()


@pytest.fixture
def mock_settings():
    """Mock settings with JWT configuration."""
    settings = Mock()
    settings.SECRET_KEY = "test-secret-key-32-chars-minimum9"
    settings.REFRESH_SECRET_KEY = "test-refresh-key-32-chars-minimum9"
    settings.ALGORITHM = "HS256"
    settings.ACCESS_TOKEN_EXPIRE_MINUTES = 30
    settings.REFRESH_TOKEN_EXPIRE_DAYS = 7
    return settings


@pytest.fixture
def jwt_handler(mock_user_repository, mock_redis_auth_repository):
    """JWT Handler instance with mocked dependencies."""
    # Set environment variables for JWT configuration
    os.environ["SECRET_KEY"] = "test-secret-key-32-chars-minimum9"
    os.environ["REFRESH_SECRET_KEY"] = "test-refresh-key-32-chars-minimum9"
    os.environ["ALGORITHM"] = "HS256"
    os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
    os.environ["REFRESH_TOKEN_EXPIRE_DAYS"] = "7"

    handler = JwtHandler(
        user_repository=mock_user_repository,
        redis_auth_respository=mock_redis_auth_repository
    )
    return handler


# ===== TOKENS =====
@pytest.fixture
def valid_access_token(jwt_handler, mock_user_entity):
    """Generate a valid access token."""
    return jwt_handler._create_access_token(
        data={"id": mock_user_entity.id, "role": mock_user_entity.is_super_admin}
    )


@pytest.fixture
def valid_refresh_token(jwt_handler, mock_user_entity):
    """Generate a valid refresh token."""
    return jwt_handler._create_refresh_token(
        data={"id": mock_user_entity.id, "role": mock_user_entity.is_super_admin}
    )


@pytest.fixture
def expired_access_token(jwt_handler, mock_user_entity):
    """Generate an expired access token."""
    with freeze_time("2026-04-15 12:00:00"):
        token = jwt_handler._create_access_token(
            data={"id": mock_user_entity.id, "role": mock_user_entity.is_super_admin},
            expires_delta=timedelta(minutes=-1)
        )
    return token


@pytest.fixture
def expired_refresh_token(jwt_handler, mock_user_entity):
    """Generate an expired refresh token."""
    with freeze_time("2026-04-15 12:00:00"):
        token = jwt_handler._create_refresh_token(
            data={"id": mock_user_entity.id, "role": mock_user_entity.is_super_admin}
        )
    return token
