"""
Root conftest.py - Shared fixtures for all tests.
All child conftest.py files inherit these fixtures.
"""
import logging
from datetime import datetime
from unittest.mock import Mock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.application.user.dtos.user_dtos import CreateUserDto, UserOutputDto
from app.domain.user.entities import User
from app.infrastructure.schemas.base import Base
from app.infrastructure.schemas.user.user_schema import UserSchema

# Suppress SQLAlchemy logging during tests for better performance
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)

# ============================================================================
# DATABASE FIXTURES - In-memory SQLite for testing
# ============================================================================

@pytest.fixture(scope="function")
def test_db_engine():
    """Create an in-memory SQLite database for testing.

    Uses optimized settings for fast test execution:
    - Disabled synchronous mode for faster writes
    - No foreign key enforcement (unless needed)
    - No query logging
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={
            "check_same_thread": False,
            "timeout": 5.0,
        },
        echo=False,
        pool_pre_ping=False,  # Disabled - not needed for in-memory DB
    )

    # Enable speed optimizations for SQLite
    with engine.connect() as conn:
        conn.exec_driver_sql("PRAGMA synchronous = OFF")
        conn.exec_driver_sql("PRAGMA journal_mode = MEMORY")
        conn.exec_driver_sql("PRAGMA foreign_keys = OFF")
        conn.commit()

    Base.metadata.create_all(engine)
    yield engine

    # Quick cleanup
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def test_db_session(test_db_engine):
    """Create a fresh database session for each test.

    Fast cleanup via transaction rollback.
    """
    connection = test_db_engine.connect()
    transaction = connection.begin_nested()

    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = TestSession()

    yield session

    # Fast cleanup via rollback instead of delete
    session.close()
    transaction.rollback()
    connection.close()


# ============================================================================
# MOCK DATA FIXTURES - User data for testing
# ============================================================================

@pytest.fixture
def mock_user_entity():
    """Create a mock User entity."""
    return User(
        id=1,
        name="John Doe",
        email="john@example.com",
        password="$argon2id$v=19$m=65540,t=3,p=4$test$test123",
        is_active=True,
        is_super_admin=False,
        creation_date=datetime(2026, 4, 1, 10, 0, 0),
        update_date=None
    )


@pytest.fixture
def mock_user_entity_list():
    """Create a list of mock User entities."""
    return [
        User(
            id=1,
            name="John Doe",
            email="john@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$test123",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime(2026, 4, 1, 10, 0, 0),
            update_date=None
        ),
        User(
            id=2,
            name="Jane Smith",
            email="jane@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$test456",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime(2026, 4, 1, 11, 0, 0),
            update_date=None
        ),
        User(
            id=3,
            name="Admin User",
            email="admin@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$test789",
            is_active=True,
            is_super_admin=True,
            creation_date=datetime(2026, 4, 1, 12, 0, 0),
            update_date=None
        ),
    ]


@pytest.fixture
def mock_create_user_dto():
    """Create a mock CreateUserDto."""
    return CreateUserDto(
        name="Test User",
        email="test@example.com",
        password="plain_password_123",
        is_active=True,
        is_super_admin=False,
        creation_date=datetime(2026, 4, 1, 10, 0, 0),
        update_date=None
    )


@pytest.fixture
def mock_user_output_dto():
    """Create a mock UserOutputDto."""
    return UserOutputDto(
        id=1,
        name="Test User",
        email="test@example.com",
        password="$argon2id$v=19$m=65540,t=3,p=4$test$test123",
        is_active=True,
        creation_date=datetime(2026, 4, 1, 10, 0, 0),
        update_date=None
    )


@pytest.fixture
def mock_user_output_dto_list():
    """Create a list of mock UserOutputDto."""
    return [
        UserOutputDto(
            id=1,
            name="John Doe",
            email="john@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$test123",
            is_active=True,
            creation_date=datetime(2026, 4, 1, 10, 0, 0),
            update_date=None
        ),
        UserOutputDto(
            id=2,
            name="Jane Smith",
            email="jane@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$test456",
            is_active=True,
            creation_date=datetime(2026, 4, 1, 11, 0, 0),
            update_date=None
        ),
    ]


@pytest.fixture
def mock_user_schema(test_db_session):
    """Create a mock UserSchema in the test database."""
    user = UserSchema(
        id=1,
        name="DB User",
        email="db@example.com",
        password="$argon2id$v=19$m=65540,t=3,p=4$test$test123",
        is_active=True,
        is_super_admin=False,
        creation_date=datetime(2026, 4, 1, 10, 0, 0),
        update_date=None
    )
    test_db_session.add(user)
    test_db_session.commit()
    test_db_session.refresh(user)
    return user


@pytest.fixture
def mock_multiple_user_schemas(test_db_session):
    """Create multiple UserSchema objects in the test database."""
    users = [
        UserSchema(
            name="User One",
            email="one@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$test1",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime(2026, 4, 1, 10, 0, 0),
            update_date=None
        ),
        UserSchema(
            name="User Two",
            email="two@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$test2",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime(2026, 4, 1, 11, 0, 0),
            update_date=None
        ),
    ]
    for user in users:
        test_db_session.add(user)
    test_db_session.commit()
    for user in users:
        test_db_session.refresh(user)
    return users


# ============================================================================
# REPOSITORY & USE CASE FIXTURES
# ============================================================================

@pytest.fixture
def mock_user_repository():
    """Create a mock user repository."""
    mock_repo = Mock()
    return mock_repo


@pytest.fixture
def mock_user_repository_with_user(mock_user_repository, mock_user_entity):
    """Mock repository that returns a single user."""
    mock_user_repository.get_users.return_value = [mock_user_entity]
    return mock_user_repository


@pytest.fixture
def mock_user_repository_with_users(mock_user_repository, mock_user_entity_list):
    """Mock repository that returns multiple users."""
    mock_user_repository.get_users.return_value = mock_user_entity_list
    return mock_user_repository


# ============================================================================
# SETTINGS & CONFIG FIXTURES
# ============================================================================

@pytest.fixture
def mock_settings():
    """Create a mock Settings object."""
    from app.settings import Settings
    return Settings(
        PROJECT_NAME="Workout-app-be",
        ROOT_PATH="/workout-app-be",
        PREFIX="/api/v1",
        DATABASE_URL="sqlite:///:memory:"
    )
