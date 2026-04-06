from datetime import datetime

import pytest
from pydantic import ValidationError

from app.application.user.dtos.user_dtos import UserOutputDto


class TestUserOutputDtoForGetUsers:
    """Test suite for UserOutputDto validation - Used in get_all_users response."""

    def test_user_output_dto_valid_data(self, mock_user_output_dto):
        """Test creating a valid UserOutputDto for get users response."""
        assert mock_user_output_dto.id == 1
        assert mock_user_output_dto.name == "Test User"
        assert mock_user_output_dto.email == "test@example.com"
        assert mock_user_output_dto.is_active is True

    def test_user_output_dto_requires_id(self):
        """Test that UserOutputDto requires id field."""
        with pytest.raises(ValidationError):
            UserOutputDto(
                # Missing id
                name="Test User",
                email="test@example.com",
                password="hashed_password",
                is_active=True,
                creation_date=datetime(2026, 4, 1, 10, 0, 0)
            )

    def test_user_output_dto_requires_name(self):
        """Test that UserOutputDto requires name field."""
        with pytest.raises(ValidationError):
            UserOutputDto(
                id=1,
                # Missing name
                email="test@example.com",
                password="hashed_password",
                is_active=True,
                creation_date=datetime(2026, 4, 1, 10, 0, 0)
            )

    def test_user_output_dto_requires_email(self):
        """Test that UserOutputDto requires email field."""
        with pytest.raises(ValidationError):
            UserOutputDto(
                id=1,
                name="Test User",
                # Missing email
                password="hashed_password",
                is_active=True,
                creation_date=datetime(2026, 4, 1, 10, 0, 0)
            )

    def test_user_output_dto_requires_password(self):
        """Test that UserOutputDto requires password field."""
        with pytest.raises(ValidationError):
            UserOutputDto(
                id=1,
                name="Test User",
                email="test@example.com",
                # Missing password
                is_active=True,
                creation_date=datetime(2026, 4, 1, 10, 0, 0)
            )

    def test_user_output_dto_requires_is_active(self):
        """Test that UserOutputDto requires is_active field."""
        with pytest.raises(ValidationError):
            UserOutputDto(
                id=1,
                name="Test User",
                email="test@example.com",
                password="hashed_password",
                # Missing is_active
                creation_date=datetime(2026, 4, 1, 10, 0, 0)
            )

    def test_user_output_dto_email_validation(self):
        """Test that UserOutputDto validates email format."""
        with pytest.raises(ValidationError):
            UserOutputDto(
                id=1,
                name="Test User",
                email="invalid-email",  # Invalid email
                password="hashed_password",
                is_active=True,
                creation_date=datetime(2026, 4, 1, 10, 0, 0)
            )

    def test_user_output_dto_valid_email_formats(self):
        """Test that UserOutputDto accepts various valid email formats."""
        emails = [
            "simple@example.com",
            "user+tag@example.com",
            "john.doe@company.co.uk"
        ]

        for email in emails:
            dto = UserOutputDto(
                id=1,
                name="Test User",
                email=email,
                password="hashed",
                is_active=True,
                creation_date=datetime(2026, 4, 1, 10, 0, 0)
            )
            assert dto.email == email

    def test_user_output_dto_is_active_as_boolean(self):
        """Test that UserOutputDto handles is_active correctly."""
        dto_active = UserOutputDto(
            id=1,
            name="Test",
            email="test@example.com",
            password="hash",
            is_active=True,
            creation_date=datetime(2026, 4, 1, 10, 0, 0)
        )

        dto_inactive = UserOutputDto(
            id=1,
            name="Test",
            email="test@example.com",
            password="hash",
            is_active=False,
            creation_date=datetime(2026, 4, 1, 10, 0, 0)
        )

        assert dto_active.is_active is True
        assert dto_inactive.is_active is False

    def test_user_output_dto_from_attributes_config(self):
        """Test that UserOutputDto can be created from ORM objects."""
        from datetime import datetime

        from app.infrastructure.schemas.user.user_schema import UserSchema

        schema = UserSchema(
            id=1,
            name="Test User",
            email="test@example.com",
            password="hashed_password",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime.now(),
            update_date=None
        )

        # Should be able to validate from ORM object
        dto = UserOutputDto.model_validate(schema)
        assert dto.id == 1
        assert dto.name == "Test User"
        assert dto.email == "test@example.com"

    def test_user_output_dto_list_validation(self, mock_user_output_dto_list):
        """Test creating a list of UserOutputDto objects."""
        assert len(mock_user_output_dto_list) == 2
        assert all(isinstance(dto, UserOutputDto) for dto in mock_user_output_dto_list)

    def test_user_output_dto_with_admin_user(self):
        """Test UserOutputDto with admin user data (from get_all_users)."""
        admin_dto = UserOutputDto(
            id=1,
            name="Admin User",
            email="admin@example.com",
            password="admin_hash",
            is_active=True,
            creation_date=datetime(2026, 4, 1, 10, 0, 0)
        )

        assert admin_dto.name == "Admin User"
        assert admin_dto.is_active is True

    def test_user_output_dto_with_inactive_user(self):
        """Test UserOutputDto with inactive user (from get_all_users)."""
        inactive_dto = UserOutputDto(
            id=1,
            name="Inactive User",
            email="inactive@example.com",
            password="hash",
            is_active=False,
            creation_date=datetime(2026, 4, 1, 10, 0, 0)
        )

        assert inactive_dto.is_active is False

    def test_user_output_dto_id_type(self):
        """Test that UserOutputDto id is integer."""
        dto = UserOutputDto(
            id=42,
            name="Test",
            email="test@example.com",
            password="hash",
            is_active=True,
            creation_date=datetime(2026, 4, 1, 10, 0, 0)
        )

        assert isinstance(dto.id, int)
        assert dto.id == 42

    def test_user_output_dto_numeric_id(self):
        """Test UserOutputDto with various numeric IDs."""
        for id_val in [1, 100, 9999]:
            dto = UserOutputDto(
                id=id_val,
                name="Test",
                email="test@example.com",
                password="hash",
                is_active=True,
                creation_date=datetime(2026, 4, 1, 10, 0, 0)
            )
            assert dto.id == id_val

    def test_user_output_dto_preserves_all_data(self):
        """Test that UserOutputDto preserves all input data."""
        dto = UserOutputDto(
            id=5,
            name="John Smith",
            email="john.smith@example.com",
            password="long_hashed_password_value",
            is_active=True,
            creation_date=datetime(2026, 4, 1, 10, 0, 0)
        )

        assert dto.id == 5
        assert dto.name == "John Smith"
        assert dto.email == "john.smith@example.com"
        assert dto.password == "long_hashed_password_value"
        assert dto.is_active is True
