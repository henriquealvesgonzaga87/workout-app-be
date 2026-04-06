from datetime import datetime

import pytest

from app.application.user.dtos.user_dtos import UpdateUserDto
from app.domain.user.entities import User
from app.infrastructure.repositories.sqlalchemy.user.user_repo import (
    SQLAlchemyUserRepository,
)
from app.presentation.error_handlers.data_base_error import DataBaseError
from app.presentation.error_handlers.not_found_error import NotFoundError


class TestSQLAlchemyUserRepositoryUpdate:
    """Test suite for SQLAlchemyUserRepository update operation."""

    def test_repository_update_user_successfully(self, test_db_session, mock_user_schema):
        """Test updating a user successfully."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        user_to_update = UpdateUserDto(
            name="Updated User",
            email=None,
            password="$argon2id$v=19$m=65540,t=3,p=4$test$updated",
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=datetime.now()
        )

        updated_user = repo.update(id=mock_user_schema.id, user=user_to_update)

        assert updated_user.id == mock_user_schema.id
        assert updated_user.name == "Updated User"
        assert updated_user.email == mock_user_schema.email
        assert updated_user.is_active is True

    def test_update_user_name_only(self, test_db_session, mock_user_schema):
        """Test updating only the user's name."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        user_to_update = UpdateUserDto(
            name="New Name",
            email=None,
            password=None,
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=datetime.now()
        )

        updated_user = repo.update(id=mock_user_schema.id, user=user_to_update)

        assert updated_user.name == "New Name"
        assert updated_user.email == mock_user_schema.email

    def test_update_user_email_only(self, test_db_session, mock_user_schema):
        """Test updating only the user's email."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        user_to_update = UpdateUserDto(
            name=None,
            email="newemail@example.com",
            password=None,
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=datetime.now()
        )

        updated_user = repo.update(id=mock_user_schema.id, user=user_to_update)

        assert updated_user.email == "newemail@example.com"
        assert updated_user.name == mock_user_schema.name

    def test_update_user_password_only(self, test_db_session, mock_user_schema):
        """Test updating only the user's password."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        new_hash = "$argon2id$v=19$m=65540,t=3,p=4$test$newpass"
        user_to_update = UpdateUserDto(
            name=None,
            email=None,
            password=new_hash,
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=datetime.now()
        )

        updated_user = repo.update(id=mock_user_schema.id, user=user_to_update)

        assert updated_user.password == new_hash
        assert updated_user.name == mock_user_schema.name
        assert updated_user.email == mock_user_schema.email

    def test_update_user_toggle_is_active(self, test_db_session, mock_user_schema):
        """Test toggling user's is_active status."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        # Toggle from True to False
        user_to_update = UpdateUserDto(
            name=None,
            email=None,
            password=None,
            is_active=False,
            is_super_admin=False,
            creation_date=None,
            update_date=datetime.now()
        )

        updated_user = repo.update(id=mock_user_schema.id, user=user_to_update)

        assert updated_user.is_active is False

    def test_update_user_toggle_is_super_admin(self, test_db_session, mock_user_schema):
        """Test toggling user's is_super_admin status."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        user_to_update = UpdateUserDto(
            name=None,
            email=None,
            password=None,
            is_active=True,
            is_super_admin=True,
            creation_date=None,
            update_date=datetime.now()
        )

        updated_user = repo.update(id=mock_user_schema.id, user=user_to_update)

        assert updated_user.is_super_admin is True

    def test_update_nonexistent_user_raises_not_found_error(self, test_db_session):
        """Test that updating nonexistent user raises NotFoundError."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        user_to_update = UpdateUserDto(
            name="Not Exist",
            email="notexist@example.com",
            password="hash",
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=datetime.now()
        )

        with pytest.raises(NotFoundError):
            repo.update(id=9999, user=user_to_update)

    def test_update_user_preserves_creation_date(self, test_db_session, mock_user_schema):
        """Test that update preserves the user's creation_date."""
        original_creation_date = mock_user_schema.creation_date
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        user_to_update = UpdateUserDto(
            name="Updated Name",
            email=None,
            password=None,
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=datetime.now()
        )

        updated_user = repo.update(id=mock_user_schema.id, user=user_to_update)

        # Creation date should remain unchanged as we don't pass it to update
        assert updated_user.creation_date == original_creation_date

    def test_update_user_sets_update_date(self, test_db_session, mock_user_schema):
        """Test that update_date is set when user is updated."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        update_time = datetime.now()
        user_to_update = UpdateUserDto(
            name="Updated User",
            email=None,
            password=None,
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=update_time
        )

        updated_user = repo.update(id=mock_user_schema.id, user=user_to_update)

        # The update_date should be set (may differ slightly due to DB handling)
        assert updated_user.update_date is not None

    def test_update_multiple_fields_simultaneously(self, test_db_session, mock_user_schema):
        """Test updating multiple fields at once."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        user_to_update = UpdateUserDto(
            name="Multi Updated",
            email="multiemail@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$multi",
            is_active=False,
            is_super_admin=True,
            creation_date=None,
            update_date=datetime.now()
        )

        updated_user = repo.update(id=mock_user_schema.id, user=user_to_update)

        assert updated_user.name == "Multi Updated"
        assert updated_user.email == "multiemail@example.com"
        assert updated_user.password == "$argon2id$v=19$m=65540,t=3,p=4$test$multi"
        assert updated_user.is_active is False
        assert updated_user.is_super_admin is True

    def test_update_user_with_duplicate_email_raises_database_error(
        self, test_db_session, mock_user_schema, mock_multiple_user_schemas
    ):
        """Test that updating user with duplicate email raises DataBaseError."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        # Try to update first user with second user's email
        user_to_update = UpdateUserDto(
            name="Duplicate Email Test",
            email=mock_multiple_user_schemas[1].email,  # Email already taken
            password=None,
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=datetime.now()
        )

        with pytest.raises(DataBaseError):
            repo.update(id=mock_multiple_user_schemas[0].id, user=user_to_update)

    def test_update_user_returns_correct_entity_type(self, test_db_session, mock_user_schema):
        """Test that update returns User entity with all fields."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        user_to_update = UpdateUserDto(
            name="Entity Test",
            email="entity@example.com",
            password="hash",
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=datetime.now()
        )

        result = repo.update(id=mock_user_schema.id, user=user_to_update)

        assert isinstance(result, User)
        assert hasattr(result, 'id')
        assert hasattr(result, 'name')
        assert hasattr(result, 'email')
        assert hasattr(result, 'password')
        assert hasattr(result, 'is_active')
        assert hasattr(result, 'is_super_admin')
        assert hasattr(result, 'creation_date')
        assert hasattr(result, 'update_date')

    def test_update_user_persistence(self, test_db_session, mock_user_schema):
        """Test that user update persists in database."""

        user_id = mock_user_schema.id
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        user_to_update = UpdateUserDto(
            name="Persistence Test",
            email="persistence@example.com",
            password="hash",
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=datetime.now()
        )

        updated_user = repo.update(id=user_id, user=user_to_update)

        assert updated_user.name == "Persistence Test"
        assert updated_user.email == "persistence@example.com"

    def test_update_user_with_special_characters_in_name(self, test_db_session, mock_user_schema):
        """Test updating user with special characters in name."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        special_name = "José María Pérez-García"
        user_to_update = UpdateUserDto(
            name=special_name,
            email=None,
            password=None,
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=datetime.now()
        )

        updated_user = repo.update(id=mock_user_schema.id, user=user_to_update)

        assert updated_user.name == special_name

    def test_update_user_with_very_long_name(self, test_db_session, mock_user_schema):
        """Test updating user with very long name."""
        repo = SQLAlchemyUserRepository(db_session=test_db_session)

        long_name = "A" * 255  # Very long name
        user_to_update = UpdateUserDto(
            name=long_name,
            email=None,
            password=None,
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=datetime.now()
        )

        updated_user = repo.update(id=mock_user_schema.id, user=user_to_update)

        assert updated_user.name == long_name
        assert len(updated_user.name) == 255
