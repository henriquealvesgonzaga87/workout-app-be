from datetime import datetime
from unittest.mock import Mock

import pytest
from pydantic import ValidationError

from app.application.user.dtos.user_dtos import UpdateUserDto, UserOutputDto
from app.application.user.use_cases.update_user_use_case import UpdateUserUseCase
from app.domain.user.entities import User
from app.presentation.error_handlers.reponse_error import ResponseError


class TestUpdateUserUseCase:
    """Test suite for UpdateUserUseCase."""

    def test_update_user_use_case_initialization(self, mock_user_repository):
        """Test that use case initializes correctly."""
        use_case = UpdateUserUseCase(user_repository=mock_user_repository)
        assert use_case.user_repository == mock_user_repository

    def test_prepare_method_hashes_password(self):
        """Test that prepare method hashes the password when provided."""
        mock_repo = Mock()
        use_case = UpdateUserUseCase(user_repository=mock_repo)

        now = datetime.now()
        update_dto = UpdateUserDto(
            name="Updated User",
            email="updated@example.com",
            password="plain_password_123",
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=now
        )

        prepared_dto = use_case.prepare(user_dto=update_dto)

        # Password should be hashed and different from original
        assert prepared_dto.password != update_dto.password
        assert len(prepared_dto.password) > len(update_dto.password)
        # Other fields should remain the same
        assert prepared_dto.name == update_dto.name
        assert prepared_dto.email == update_dto.email

    def test_prepare_method_preserves_none_password(self):
        """Test that prepare method preserves None password without hashing."""
        mock_repo = Mock()
        use_case = UpdateUserUseCase(user_repository=mock_repo)

        now = datetime.now()
        update_dto = UpdateUserDto(
            name="Updated User",
            email="updated@example.com",
            password=None,
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=now
        )

        prepared_dto = use_case.prepare(user_dto=update_dto)

        # Password should remain None
        assert prepared_dto.password is None
        assert prepared_dto.name == update_dto.name

    def test_prepare_method_preserves_user_data(self):
        """Test that prepare method preserves all other user data."""
        mock_repo = Mock()
        use_case = UpdateUserUseCase(user_repository=mock_repo)

        now = datetime.now()
        update_dto = UpdateUserDto(
            name="Updated User",
            email="updated@example.com",
            password=None,
            is_active=False,
            is_super_admin=True,
            creation_date=None,
            update_date=now
        )

        prepared_dto = use_case.prepare(user_dto=update_dto)

        assert prepared_dto.name == update_dto.name
        assert prepared_dto.email == update_dto.email
        assert prepared_dto.is_active == update_dto.is_active
        assert prepared_dto.is_super_admin == update_dto.is_super_admin
        assert prepared_dto.update_date == update_dto.update_date

    def test_execute_updates_user_successfully(self, mock_user_repository):
        """Test successful user update."""
        # Create the user to be updated
        updated_user = User(
            id=1,
            name="Updated User",
            email="updated@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$updated",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime(2026, 1, 1, 10, 0, 0),
            update_date=datetime.now()
        )
        mock_user_repository.update.return_value = updated_user

        use_case = UpdateUserUseCase(user_repository=mock_user_repository)

        now = datetime.now()
        update_dto = UpdateUserDto(
            name="Updated User",
            email="updated@example.com",
            password="plain_password",
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=now
        )

        result = use_case.execute(id=1, user_dto=update_dto)

        assert isinstance(result, UserOutputDto)
        assert result.name == "Updated User"
        assert result.email == "updated@example.com"
        assert result.id == 1
        mock_user_repository.update.assert_called_once()

    def test_execute_returns_user_output_dto(self, mock_user_repository):
        """Test that execute returns UserOutputDto with correct data."""
        updated_user = User(
            id=42,
            name="Updated Name",
            email="newemail@example.com",
            password="hashed",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime(2026, 1, 1, 10, 0, 0),
            update_date=datetime.now()
        )
        mock_user_repository.update.return_value = updated_user

        use_case = UpdateUserUseCase(user_repository=mock_user_repository)

        now = datetime.now()
        update_dto = UpdateUserDto(
            name="Updated Name",
            email="newemail@example.com",
            password="password",
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=now
        )

        result = use_case.execute(id=42, user_dto=update_dto)

        assert isinstance(result, UserOutputDto)
        assert result.id == 42
        assert result.name == "Updated Name"
        assert result.email == "newemail@example.com"

    def test_execute_with_partial_update(self, mock_user_repository):
        """Test updating user with only some fields."""
        updated_user = User(
            id=5,
            name="Original Name",
            email="newemail@example.com",
            password="original_password",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime(2026, 2, 1, 10, 0, 0),
            update_date=datetime.now()
        )
        mock_user_repository.update.return_value = updated_user

        use_case = UpdateUserUseCase(user_repository=mock_user_repository)

        now = datetime.now()
        # Only update email, keep other fields unchanged
        update_dto = UpdateUserDto(
            name=None,
            email="newemail@example.com",
            password=None,
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=now
        )

        result = use_case.execute(id=5, user_dto=update_dto)

        assert isinstance(result, UserOutputDto)
        assert result.email == "newemail@example.com"
        mock_user_repository.update.assert_called_once()

    def test_execute_calls_repository_with_correct_id(self, mock_user_repository):
        """Test that execute calls repository with the correct user ID."""
        updated_user = User(
            id=99,
            name="Test",
            email="test@example.com",
            password="hash",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime.now(),
            update_date=None
        )
        mock_user_repository.update.return_value = updated_user

        use_case = UpdateUserUseCase(user_repository=mock_user_repository)

        now = datetime.now()
        update_dto = UpdateUserDto(
            name="Test",
            email="test@example.com",
            password="password",
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=now
        )

        use_case.execute(id=99, user_dto=update_dto)

        # Verify repository was called with correct ID
        call_args = mock_user_repository.update.call_args
        assert call_args[1]['id'] == 99

    def test_execute_toggles_is_active(self, mock_user_repository):
        """Test updating user's is_active status."""
        updated_user = User(
            id=10,
            name="Test User",
            email="test@example.com",
            password="hash",
            is_active=False,
            is_super_admin=False,
            creation_date=datetime.now(),
            update_date=datetime.now()
        )
        mock_user_repository.update.return_value = updated_user

        use_case = UpdateUserUseCase(user_repository=mock_user_repository)

        now = datetime.now()
        update_dto = UpdateUserDto(
            name=None,
            email=None,
            password=None,
            is_active=False,
            is_super_admin=False,
            creation_date=None,
            update_date=now
        )

        result = use_case.execute(id=10, user_dto=update_dto)

        assert result.is_active is False

    def test_execute_toggles_is_super_admin(self, mock_user_repository):
        """Test updating user's is_super_admin status."""
        # Note: is_super_admin is not included in UserOutputDto, so we can't check it in the output
        # But we can verify it's passed to the repository
        updated_user = User(
            id=11,
            name="Admin User",
            email="admin@example.com",
            password="hash",
            is_active=True,
            is_super_admin=True,
            creation_date=datetime.now(),
            update_date=datetime.now()
        )
        mock_user_repository.update.return_value = updated_user

        use_case = UpdateUserUseCase(user_repository=mock_user_repository)

        now = datetime.now()
        update_dto = UpdateUserDto(
            name=None,
            email=None,
            password=None,
            is_active=True,
            is_super_admin=True,
            creation_date=None,
            update_date=now
        )

        use_case.execute(id=11, user_dto=update_dto)

        # Verify the call was made with correct is_super_admin flag
        call_args = mock_user_repository.update.call_args
        assert call_args[1]['user'].is_super_admin is True

    def test_execute_with_validation_error_in_prepare(self):
        """Test that invalid email raises validation error during DTO creation."""
        # The validation happens at Pydantic level during DTO creation
        with pytest.raises(ValidationError):
            UpdateUserDto(
                name="Test",
                email="invalid-email",  # Invalid email format
                password=None,
                is_active=True,
                is_super_admin=False,
                creation_date=None,
                update_date=datetime.now()
            )

    def test_execute_with_validation_error_in_repository(self, mock_user_repository):
        """Test that validation error from repository is wrapped in ResponseError."""
        mock_user_repository.update.side_effect = ValidationError.from_exception_data("test", [])

        use_case = UpdateUserUseCase(user_repository=mock_user_repository)

        now = datetime.now()
        valid_dto = UpdateUserDto(
            name="Test",
            email="test@example.com",
            password="password",
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=now
        )

        with pytest.raises(ResponseError):
            use_case.execute(id=1, user_dto=valid_dto)

    def test_execute_preserves_all_fields_in_output(self, mock_user_repository):
        """Test that all fields are preserved in the output."""
        creation_date = datetime(2026, 1, 1, 10, 0, 0)
        update_date = datetime(2026, 2, 1, 15, 30, 0)

        updated_user = User(
            id=123,
            name="Complete User",
            email="complete@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$complete",
            is_active=True,
            is_super_admin=False,
            creation_date=creation_date,
            update_date=update_date
        )
        mock_user_repository.update.return_value = updated_user

        use_case = UpdateUserUseCase(user_repository=mock_user_repository)

        update_dto = UpdateUserDto(
            name="Complete User",
            email="complete@example.com",
            password="password",
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=update_date
        )

        result = use_case.execute(id=123, user_dto=update_dto)

        assert result.id == 123
        assert result.name == "Complete User"
        assert result.email == "complete@example.com"
        assert result.is_active is True
        assert result.creation_date == creation_date
        assert result.update_date == update_date

    def test_execute_multiple_updates_on_same_user(self, mock_user_repository):
        """Test updating the same user multiple times."""
        # First update: change name
        user_after_first_update = User(
            id=50,
            name="First Update",
            email="original@example.com",
            password="hash1",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime.now(),
            update_date=datetime.now()
        )

        # Second update: change email
        user_after_second_update = User(
            id=50,
            name="First Update",
            email="second@example.com",
            password="hash1",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime.now(),
            update_date=datetime.now()
        )

        mock_user_repository.update.side_effect = [user_after_first_update, user_after_second_update]

        use_case = UpdateUserUseCase(user_repository=mock_user_repository)

        # First update
        first_dto = UpdateUserDto(
            name="First Update",
            email=None,
            password=None,
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=datetime.now()
        )
        result1 = use_case.execute(id=50, user_dto=first_dto)
        assert result1.name == "First Update"

        # Second update
        second_dto = UpdateUserDto(
            name=None,
            email="second@example.com",
            password=None,
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=datetime.now()
        )
        result2 = use_case.execute(id=50, user_dto=second_dto)
        assert result2.email == "second@example.com"
        assert mock_user_repository.update.call_count == 2
