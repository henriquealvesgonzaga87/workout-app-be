from datetime import datetime

import pytest
from pydantic import ValidationError

from app.application.user.dtos.user_dtos import UpdateUserDto, UserOutputDto


class TestUpdateUserDto:
    """Test suite for UpdateUserDto validation."""

    def test_update_user_dto_valid_data_all_fields(self):
        """Test creating a valid UpdateUserDto with all fields."""
        now = datetime.now()
        dto = UpdateUserDto(
            name="Updated User",
            email="updated@example.com",
            password="new_password_123",
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=now
        )
        assert dto.name == "Updated User"
        assert dto.email == "updated@example.com"
        assert dto.password == "new_password_123"
        assert dto.is_active is True
        assert dto.is_super_admin is False
        assert dto.update_date == now

    def test_update_user_dto_valid_data_partial_fields(self):
        """Test creating UpdateUserDto with only some fields."""
        now = datetime.now()
        dto = UpdateUserDto(
            name="Updated User",
            email=None,
            password=None,
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=now
        )
        assert dto.name == "Updated User"
        assert dto.email is None
        assert dto.password is None

    def test_update_user_dto_email_validation(self):
        """Test that invalid email format is rejected."""
        now = datetime.now()
        with pytest.raises(ValidationError):
            UpdateUserDto(
                name="Test User",
                email="invalid-email",
                password=None,
                is_active=True,
                is_super_admin=False,
                creation_date=None,
                update_date=now
            )

    def test_update_user_dto_only_name_update(self):
        """Test updating only the name field."""
        now = datetime.now()
        dto = UpdateUserDto(
            name="New Name Only",
            email=None,
            password=None,
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=now
        )
        assert dto.name == "New Name Only"
        assert dto.email is None
        assert dto.password is None

    def test_update_user_dto_only_email_update(self):
        """Test updating only the email field."""
        now = datetime.now()
        dto = UpdateUserDto(
            name=None,
            email="newemail@example.com",
            password=None,
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=now
        )
        assert dto.name is None
        assert dto.email == "newemail@example.com"
        assert dto.password is None

    def test_update_user_dto_only_password_update(self):
        """Test updating only the password field."""
        now = datetime.now()
        dto = UpdateUserDto(
            name=None,
            email=None,
            password="new_password_456",
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=now
        )
        assert dto.name is None
        assert dto.email is None
        assert dto.password == "new_password_456"

    def test_update_user_dto_toggle_is_active(self):
        """Test toggling the is_active flag."""
        now = datetime.now()
        # Test setting to False
        dto_inactive = UpdateUserDto(
            name=None,
            email=None,
            password=None,
            is_active=False,
            is_super_admin=False,
            creation_date=None,
            update_date=now
        )
        assert dto_inactive.is_active is False

        # Test setting to True
        dto_active = UpdateUserDto(
            name=None,
            email=None,
            password=None,
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=now
        )
        assert dto_active.is_active is True

    def test_update_user_dto_toggle_is_super_admin(self):
        """Test toggling the is_super_admin flag."""
        now = datetime.now()
        # Test setting to True
        dto_admin = UpdateUserDto(
            name=None,
            email=None,
            password=None,
            is_active=True,
            is_super_admin=True,
            creation_date=None,
            update_date=now
        )
        assert dto_admin.is_super_admin is True

        # Test setting to False
        dto_non_admin = UpdateUserDto(
            name=None,
            email=None,
            password=None,
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=now
        )
        assert dto_non_admin.is_super_admin is False

    def test_update_user_dto_missing_update_date(self):
        """Test that missing update_date raises validation error."""
        with pytest.raises(ValidationError):
            UpdateUserDto(
                name="Test User",
                email=None,
                password=None,
                is_active=True,
                is_super_admin=False,
                creation_date=None
                # update_date is missing
            )

    def test_update_user_dto_empty_name(self):
        """Test that empty name is allowed."""
        now = datetime.now()
        dto = UpdateUserDto(
            name="",
            email=None,
            password=None,
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=now
        )
        assert dto.name == ""

    def test_update_user_dto_very_long_name(self):
        """Test handling of very long name string."""
        now = datetime.now()
        long_name = "A" * 500  # 500 character name
        dto = UpdateUserDto(
            name=long_name,
            email=None,
            password=None,
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=now
        )
        assert dto.name == long_name
        assert len(dto.name) == 500

    def test_update_user_dto_preserve_creation_date(self):
        """Test that creation_date can be None for updates."""
        now = datetime.now()
        dto = UpdateUserDto(
            name="Updated User",
            email="updated@example.com",
            password="new_password",
            is_active=True,
            is_super_admin=False,
            creation_date=None,
            update_date=now
        )
        assert dto.creation_date is None

    def test_update_user_dto_set_creation_date(self):
        """Test that creation_date can be set explicitly."""
        now = datetime.now()
        past_date = datetime(2026, 1, 1, 10, 0, 0)
        dto = UpdateUserDto(
            name="Updated User",
            email="updated@example.com",
            password="new_password",
            is_active=True,
            is_super_admin=False,
            creation_date=past_date,
            update_date=now
        )
        assert dto.creation_date == past_date

    def test_update_user_output_dto_valid_data(self):
        """Test UserOutputDto with valid data."""
        output_dto = UserOutputDto(
            id=1,
            name="Test User",
            email="test@example.com",
            password="hashed_password",
            is_active=True,
            creation_date=datetime.now()
        )
        assert output_dto.id == 1
        assert output_dto.name == "Test User"
        assert output_dto.email == "test@example.com"
        assert output_dto.is_active is True

    def test_update_user_output_dto_with_update_date(self):
        """Test UserOutputDto with update_date set."""
        now = datetime.now()
        output_dto = UserOutputDto(
            id=5,
            name="Updated User",
            email="updated@example.com",
            password="hashed_password",
            is_active=True,
            creation_date=datetime(2026, 1, 1, 10, 0, 0),
            update_date=now
        )
        assert output_dto.update_date == now
        assert output_dto.id == 5

    def test_update_user_output_dto_inactive_user(self):
        """Test UserOutputDto with inactive user."""
        output_dto = UserOutputDto(
            id=10,
            name="Inactive User",
            email="inactive@example.com",
            password="hashed_password",
            is_active=False,
            creation_date=datetime.now()
        )
        assert output_dto.is_active is False
