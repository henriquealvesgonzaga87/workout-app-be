from datetime import datetime

from app.application.user.dtos.user_dtos import UpdateUserDto, UserOutputDto
from app.presentation.mappers.user.mappers import UserMapper
from app.presentation.models.user.create_user_model import (
    CreateUserResponse,
    UpdateUserRequest,
)


class TestUserMapperUpdateUser:
    """Test suite for UserMapper with update user functionality."""

    def test_to_application_dto_update_conversion(self):
        """Test converting UpdateUserRequest to UpdateUserDto."""
        request = UpdateUserRequest(
            name="Updated User",
            email="updated@example.com",
            password="new_password123"
        )

        dto = UserMapper.to_application_dto_update(user_request_data=request)

        assert isinstance(dto, UpdateUserDto)
        assert dto.name == request.name
        assert dto.email == request.email
        assert dto.password == request.password
        assert dto.is_active is True
        assert dto.is_super_admin is False

    def test_to_application_dto_update_with_none_values(self):
        """Test converting UpdateUserRequest with None values."""
        request = UpdateUserRequest(
            name=None,
            email="new@example.com",
            password=None
        )

        dto = UserMapper.to_application_dto_update(user_request_data=request)

        assert isinstance(dto, UpdateUserDto)
        assert dto.name is None
        assert dto.email == "new@example.com"
        assert dto.password is None
        assert dto.is_active is True

    def test_to_application_dto_update_sets_update_date(self):
        """Test that to_application_dto_update sets update_date."""
        before = datetime.utcnow()
        request = UpdateUserRequest(
            name="Test User",
            email="test@example.com",
            password="password123"
        )

        dto = UserMapper.to_application_dto_update(user_request_data=request)
        after = datetime.utcnow()

        assert before <= dto.update_date <= after

    def test_to_application_dto_update_sets_defaults(self):
        """Test that to_application_dto_update sets default values."""
        request = UpdateUserRequest(
            name="Test User",
            email="test@example.com",
            password="password123"
        )

        dto = UserMapper.to_application_dto_update(user_request_data=request)

        # Default values should be set
        assert dto.is_active is True
        assert dto.is_super_admin is False
        assert dto.creation_date is None
        assert dto.update_date is not None

    def test_to_application_dto_update_only_name(self):
        """Test updating only the name field."""
        request = UpdateUserRequest(
            name="New Name",
            email=None,
            password=None
        )

        dto = UserMapper.to_application_dto_update(user_request_data=request)

        assert dto.name == "New Name"
        assert dto.email is None
        assert dto.password is None

    def test_to_application_dto_update_only_email(self):
        """Test updating only the email field."""
        request = UpdateUserRequest(
            name=None,
            email="newemail@example.com",
            password=None
        )

        dto = UserMapper.to_application_dto_update(user_request_data=request)

        assert dto.name is None
        assert dto.email == "newemail@example.com"
        assert dto.password is None

    def test_to_application_dto_update_only_password(self):
        """Test updating only the password field."""
        request = UpdateUserRequest(
            name=None,
            email=None,
            password="new_password_456"
        )

        dto = UserMapper.to_application_dto_update(user_request_data=request)

        assert dto.name is None
        assert dto.email is None
        assert dto.password == "new_password_456"

    def test_to_application_dto_update_all_none(self):
        """Test updating with all None values."""
        request = UpdateUserRequest(
            name=None,
            email=None,
            password=None
        )

        dto = UserMapper.to_application_dto_update(user_request_data=request)

        assert dto.name is None
        assert dto.email is None
        assert dto.password is None
        assert dto.is_active is True
        assert dto.is_super_admin is False

    def test_to_web_response_conversion_with_updated_user(self):
        """Test converting updated UserOutputDto to CreateUserResponse."""
        output_dto = UserOutputDto(
            id=1,
            name="Updated User",
            email="updated@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$test123",
            is_active=True,
            creation_date=datetime(2026, 4, 1, 10, 0, 0)
        )
        response = UserMapper.to_web_response(user_output_dto=output_dto)

        assert isinstance(response, CreateUserResponse)
        assert response.id == output_dto.id
        assert response.name == output_dto.name
        assert response.email == output_dto.email
        assert response.password == output_dto.password
        assert response.is_active == output_dto.is_active

    def test_to_web_response_preserves_all_update_fields(self):
        """Test that to_web_response preserves all updated fields."""
        now = datetime.now()
        output_dto = UserOutputDto(
            id=42,
            name="Updated User",
            email="updated@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$hash",
            is_active=True,
            creation_date=datetime(2026, 1, 1, 10, 0, 0),
            update_date=now
        )

        response = UserMapper.to_web_response(user_output_dto=output_dto)

        assert response.id == 42
        assert response.name == "Updated User"
        assert response.email == "updated@example.com"
        assert response.password == "$argon2id$v=19$m=65540,t=3,p=4$test$hash"
        assert response.is_active is True
        assert response.update_date == now

    def test_to_web_response_with_deactivated_user(self):
        """Test converting deactivated user to response."""
        output_dto = UserOutputDto(
            id=1,
            name="Deactivated User",
            email="deactivated@example.com",
            password="hash",
            is_active=False,
            creation_date=datetime(2026, 4, 1, 10, 0, 0),
            update_date=datetime(2026, 4, 2, 10, 0, 0)
        )

        response = UserMapper.to_web_response(user_output_dto=output_dto)

        assert response.is_active is False
        assert response.id == 1

    def test_mapper_update_request_email_validation(self):
        """Test that mapper respects email validation in UpdateUserRequest."""
        # UpdateUserRequest should accept None email
        request = UpdateUserRequest(
            name="Test",
            email=None,
            password="password"
        )

        # Convert to DTO
        dto = UserMapper.to_application_dto_update(user_request_data=request)
        assert dto.email is None

    def test_mapper_chain_update_request_to_response(self):
        """Test the complete chain from UpdateUserRequest to CreateUserResponse."""
        # Create update request
        request = UpdateUserRequest(
            name="Full Chain Test",
            email="fullchain@example.com",
            password="password123"
        )

        # Convert to application DTO
        dto = UserMapper.to_application_dto_update(user_request_data=request)

        # Simulate getting output DTO from use case
        output_dto = UserOutputDto(
            id=99,
            name=dto.name or "Original Name",
            email=dto.email or "original@example.com",
            password="hashed_password",
            is_active=True,
            creation_date=datetime(2026, 4, 1, 10, 0, 0),
            update_date=dto.update_date
        )

        # Convert to response
        response = UserMapper.to_web_response(user_output_dto=output_dto)

        assert response.id == 99
        assert response.name == "Full Chain Test"
        assert response.email == "fullchain@example.com"
        assert isinstance(response, CreateUserResponse)

    def test_mapper_preserves_special_characters(self):
        """Test that mapper preserves special characters in names and emails."""
        request = UpdateUserRequest(
            name="José García",
            email="josé.garcía@example.com",
            password="password123"
        )

        dto = UserMapper.to_application_dto_update(user_request_data=request)

        assert dto.name == "José García"
        assert dto.email == "josé.garcía@example.com"

    def test_mapper_handles_long_strings(self):
        """Test that mapper handles very long strings."""
        long_name = "A" * 500
        request = UpdateUserRequest(
            name=long_name,
            email="test@example.com",
            password="password"
        )

        dto = UserMapper.to_application_dto_update(user_request_data=request)

        assert dto.name == long_name
        assert len(dto.name) == 500
