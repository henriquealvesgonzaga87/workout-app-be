"""Fixtures and configuration for redis auth tests."""

from unittest.mock import Mock

import pytest

from app.application.redis.auth.interfaces.interfaces import RedisAuthRepositoryInterface


# ===== MOCKS & REPOSITORIES =====
@pytest.fixture
def mock_redis_auth_repository():
    """Mock redis auth repository."""
    return Mock(spec=RedisAuthRepositoryInterface)


@pytest.fixture
def mock_refresh_token():
    """Mock refresh token."""
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6ZmFsc2UsImV4cCI6MTcxNDU4MDAwMH0.test_signature"


@pytest.fixture
def mock_invalid_token():
    """Mock invalid refresh token."""
    return "invalid_token_format"


@pytest.fixture
def mock_expires_in():
    """Mock expires in value (days)."""
    return 7


@pytest.fixture
def mock_long_expires_in():
    """Mock expires in value with extended duration."""
    return 30
