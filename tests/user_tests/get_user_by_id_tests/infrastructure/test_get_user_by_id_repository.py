import pytest

from app.infrastructure.repositories.sqlalchemy.user.user_repo import SQLAlchemyUserRepository
from app.infrastructure.schemas.user.user_schema import UserSchema
from app.presentation.error_handlers.not_found_error import NotFoundError


class TestGetUserByIdRepository:
    """Test suite for SQLAlchemyUserRepository.get_by_id() - Infrastructure layer."""

    def test_get_by_id_returns_user_schema(self, test_db_session, mock_user_schema):
        """Test that get_by_id returns a UserSchema object."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)
        result = repo.get_by_id(id=mock_user_schema.id)

        assert result is not None
        assert hasattr(result, 'id')
        assert hasattr(result, 'name')
        assert hasattr(result, 'email')

    def test_get_by_id_returns_correct_user(self, test_db_session, mock_user_schema):
        """Test that get_by_id returns the correct user by ID."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)
        result = repo.get_by_id(id=mock_user_schema.id)

        assert result.id == mock_user_schema.id
        assert result.name == mock_user_schema.name
        assert result.email == mock_user_schema.email

    def test_get_by_id_with_nonexistent_id_raises_not_found_error(self, test_db_session):
        """Test that get_by_id raises NotFoundError for nonexistent ID."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        with pytest.raises(NotFoundError) as exc_info:
            repo.get_by_id(id=999)

        assert "User with ID 999 not found" in str(exc_info.value)

    def test_get_by_id_preserves_all_user_fields(self, test_db_session):
        """Test that get_by_id preserves all user fields."""
        from datetime import datetime

        user = UserSchema(
            name="Full User",
            email="full@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$test123",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime(2026, 4, 1, 10, 0, 0),
            update_date=None
        )
        test_db_session.add(user)
        test_db_session.commit()

        repo = SQLAlchemyUserRepository(db_session=test_db_session)
        result = repo.get_by_id(id=user.id)

        assert result.id == user.id
        assert result.name == user.name
        assert result.email == user.email
        assert result.password == user.password
        assert result.is_active == user.is_active
        assert result.is_super_admin == user.is_super_admin

    def test_get_by_id_with_unicode_name(self, test_db_session):
        """Test that get_by_id handles unicode characters in user name."""
        from datetime import datetime

        user = UserSchema(
            name="João Silva 中文",
            email="unicode@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$unicode123",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime(2026, 4, 1, 10, 0, 0),
            update_date=None
        )
        test_db_session.add(user)
        test_db_session.commit()

        repo = SQLAlchemyUserRepository(db_session=test_db_session)
        result = repo.get_by_id(id=user.id)

        assert result.name == "João Silva 中文"

    def test_get_by_id_with_active_user(self, test_db_session):
        """Test get_by_id with an active user."""
        from datetime import datetime

        user = UserSchema(
            name="Active User",
            email="active@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$active123",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime(2026, 4, 1, 10, 0, 0),
            update_date=None
        )
        test_db_session.add(user)
        test_db_session.commit()

        repo = SQLAlchemyUserRepository(db_session=test_db_session)
        result = repo.get_by_id(id=user.id)

        assert result.is_active is True

    def test_get_by_id_with_inactive_user(self, test_db_session):
        """Test get_by_id with an inactive user."""
        from datetime import datetime

        user = UserSchema(
            name="Inactive User",
            email="inactive@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$inactive123",
            is_active=False,
            is_super_admin=False,
            creation_date=datetime(2026, 4, 1, 10, 0, 0),
            update_date=None
        )
        test_db_session.add(user)
        test_db_session.commit()

        repo = SQLAlchemyUserRepository(db_session=test_db_session)
        result = repo.get_by_id(id=user.id)

        assert result.is_active is False

    def test_get_by_id_with_admin_user(self, test_db_session):
        """Test get_by_id with a super_admin user."""
        from datetime import datetime

        user = UserSchema(
            name="Admin User",
            email="admin@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$admin123",
            is_active=True,
            is_super_admin=True,
            creation_date=datetime(2026, 4, 1, 10, 0, 0),
            update_date=None
        )
        test_db_session.add(user)
        test_db_session.commit()

        repo = SQLAlchemyUserRepository(db_session=test_db_session)
        result = repo.get_by_id(id=user.id)

        assert result.is_super_admin is True

    def test_get_by_id_with_zero_id_raises_not_found_error(self, test_db_session):
        """Test that get_by_id raises NotFoundError for ID 0."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        with pytest.raises(NotFoundError):
            repo.get_by_id(id=0)

    def test_get_by_id_with_negative_id_raises_not_found_error(self, test_db_session):
        """Test that get_by_id raises NotFoundError for negative ID."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        with pytest.raises(NotFoundError):
            repo.get_by_id(id=-1)

    def test_get_by_id_with_multiple_users_returns_correct_one(self, test_db_session):
        """Test that get_by_id returns correct user when multiple users exist."""
        from datetime import datetime

        user1 = UserSchema(
            name="User One",
            email="one@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$test1",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime(2026, 4, 1, 10, 0, 0),
            update_date=None
        )
        user2 = UserSchema(
            name="User Two",
            email="two@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$test2",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime(2026, 4, 1, 11, 0, 0),
            update_date=None
        )
        test_db_session.add(user1)
        test_db_session.add(user2)
        test_db_session.commit()

        repo = SQLAlchemyUserRepository(db_session=test_db_session)
        result = repo.get_by_id(id=user2.id)

        assert result.id == user2.id
        assert result.name == "User Two"
        assert result.email == "two@example.com"

    def test_get_by_id_does_not_modify_user(self, test_db_session, mock_user_schema):
        """Test that get_by_id does not modify the user data."""
        original_name = mock_user_schema.name
        original_email = mock_user_schema.email

        repo = SQLAlchemyUserRepository(db_session=test_db_session)
        repo.get_by_id(id=mock_user_schema.id)

        # User data should remain unchanged
        assert mock_user_schema.name == original_name
        assert mock_user_schema.email == original_email
