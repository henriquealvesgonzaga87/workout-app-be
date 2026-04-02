from datetime import datetime

import pytest

from app.infrastructure.repositories.sqlalchemy.user.user_repo import SQLAlchemyUserRepository
from app.infrastructure.schemas.user.user_schema import UserSchema
from app.presentation.error_handlers.not_found_error import NotFoundError


class TestGetUsersRepository:
    """Test suite for SQLAlchemyUserRepository.get_users() - Infrastructure layer for 'get users'."""

    def test_get_users_returns_list(self, test_db_session, mock_multiple_user_schemas):
        """Test that get_users returns a list."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        result = repo.get_users()

        assert isinstance(result, list)

    def test_get_users_returns_user_entities(self, test_db_session, mock_multiple_user_schemas):
        """Test that get_users returns user data (UserSchema with User-like properties)."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        result = repo.get_users()

        assert len(result) == 2
        # Objects should have User-like properties (from UserSchema)
        assert all(hasattr(user, 'id') and hasattr(user, 'name') for user in result)

    def test_get_users_with_single_user(self, test_db_session):
        """Test get_users when only one user exists in database."""
        # Add single user
        user = UserSchema(
            name="Single User",
            email="single@example.com",
            password="hash",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime.now(),
            update_date=None
        )
        test_db_session.add(user)
        test_db_session.commit()

        repo = SQLAlchemyUserRepository(db_session=test_db_session)
        result = repo.get_users()

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].name == "Single User"

    def test_get_users_with_multiple_users(self, test_db_session, mock_multiple_user_schemas):
        """Test get_users returns all users from database."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        result = repo.get_users()

        assert len(result) == 2
        assert result[0].name == "User One"
        assert result[1].name == "User Two"

    def test_get_users_raises_not_found_when_empty(self, test_db_session):
        """Test that get_users raises NotFoundError when database is empty."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        with pytest.raises(NotFoundError) as exc_info:
            repo.get_users()

        assert "No result found" in str(exc_info.value)

    def test_get_users_returns_correct_user_data(self, test_db_session, mock_multiple_user_schemas):
        """Test that get_users returns correct user data from database."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        result = repo.get_users()

        # Verify first user
        assert result[0].id is not None
        assert result[0].name == "User One"
        assert result[0].email == "one@example.com"
        assert result[0].is_active is True
        assert result[0].is_super_admin is False

        # Verify second user
        assert result[1].name == "User Two"
        assert result[1].email == "two@example.com"

    def test_get_users_preserves_field_mapping(self, test_db_session):
        """Test that get_users correctly maps schema to User entity."""
        # Create user with all fields
        user_schema = UserSchema(
            name="Test User",
            email="test@example.com",
            password="hashed_password",
            is_active=False,
            is_super_admin=True,
            creation_date=datetime(2026, 4, 1, 10, 30, 0),
            update_date=datetime(2026, 4, 2, 15, 45, 0)
        )
        test_db_session.add(user_schema)
        test_db_session.commit()

        repo = SQLAlchemyUserRepository(db_session=test_db_session)
        result = repo.get_users()

        user = result[0]
        assert user.name == "Test User"
        assert user.email == "test@example.com"
        assert user.password == "hashed_password"
        assert user.is_active is False
        assert user.is_super_admin is True
        assert user.creation_date == datetime(2026, 4, 1, 10, 30, 0)
        assert user.update_date == datetime(2026, 4, 2, 15, 45, 0)

    def test_get_users_handles_inactive_users(self, test_db_session):
        """Test that get_users correctly retrieves inactive users."""
        # Add both active and inactive users
        users_data = [
            UserSchema(
                name="Active User",
                email="active@example.com",
                password="hash",
                is_active=True,
                is_super_admin=False,
                creation_date=datetime.now(),
                update_date=None
            ),
            UserSchema(
                name="Inactive User",
                email="inactive@example.com",
                password="hash",
                is_active=False,
                is_super_admin=False,
                creation_date=datetime.now(),
                update_date=None
            ),
        ]
        for user in users_data:
            test_db_session.add(user)
        test_db_session.commit()

        repo = SQLAlchemyUserRepository(db_session=test_db_session)
        result = repo.get_users()

        assert len(result) == 2
        assert result[0].is_active is True
        assert result[1].is_active is False

    def test_get_users_handles_admin_users(self, test_db_session):
        """Test that get_users correctly retrieves admin users."""
        # Add both regular and admin users
        users_data = [
            UserSchema(
                name="Regular User",
                email="regular@example.com",
                password="hash",
                is_active=True,
                is_super_admin=False,
                creation_date=datetime.now(),
                update_date=None
            ),
            UserSchema(
                name="Admin User",
                email="admin@example.com",
                password="hash",
                is_active=True,
                is_super_admin=True,
                creation_date=datetime.now(),
                update_date=None
            ),
        ]
        for user in users_data:
            test_db_session.add(user)
        test_db_session.commit()

        repo = SQLAlchemyUserRepository(db_session=test_db_session)
        result = repo.get_users()

        assert len(result) == 2
        assert result[0].is_super_admin is False
        assert result[1].is_super_admin is True

    def test_get_users_preserves_order(self, test_db_session):
        """Test that get_users preserves the order of users from database."""
        # Add users in specific order
        for i in range(3, 0, -1):  # Add in reverse order: 3, 2, 1
            user = UserSchema(
                name=f"User {i}",
                email=f"user{i}@example.com",
                password="hash",
                is_active=True,
                is_super_admin=False,
                creation_date=datetime.now(),
                update_date=None
            )
            test_db_session.add(user)
        test_db_session.commit()

        repo = SQLAlchemyUserRepository(db_session=test_db_session)
        result = repo.get_users()

        # Should return in order they were inserted (3, 2, 1)
        assert result[0].name == "User 3"
        assert result[1].name == "User 2"
        assert result[2].name == "User 1"

    def test_get_users_with_unicode_names(self, test_db_session):
        """Test that get_users handles unicode characters in names."""
        users_data = [
            UserSchema(
                name="José da Silva",
                email="jose@example.com",
                password="hash",
                is_active=True,
                is_super_admin=False,
                creation_date=datetime.now(),
                update_date=None
            ),
            UserSchema(
                name="北京 李明",
                email="beijing@example.com",
                password="hash",
                is_active=True,
                is_super_admin=False,
                creation_date=datetime.now(),
                update_date=None
            ),
        ]
        for user in users_data:
            test_db_session.add(user)
        test_db_session.commit()

        repo = SQLAlchemyUserRepository(db_session=test_db_session)
        result = repo.get_users()

        assert len(result) == 2
        assert result[0].name == "José da Silva"
        assert result[1].name == "北京 李明"
