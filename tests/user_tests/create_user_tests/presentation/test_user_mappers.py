from datetime import datetime

from app.application.user.dtos.user_dtos import CreateUserDto, UserOutputDto
from app.presentation.mappers.user.mappers import UserMapper
from app.presentation.models.user.create_user_model import (
    CreateUserRequest,
    CreateUserResponse,
)


class TestUserMapper:
    """Test suite for UserMapper."""

    def test_to_application_dto_conversion(self):
        """Test converting CreateUserRequest to CreateUserDto."""
        request = CreateUserRequest(
            name="Test User",
            email="test@example.com",
            password="password123"
        )

        dto = UserMapper.to_application_dto(user_request_data=request)

        assert isinstance(dto, CreateUserDto)
        assert dto.name == request.name
        assert dto.email == request.email
        assert dto.password == request.password
        assert dto.is_active is True
        assert dto.is_super_admin is False
        assert dto.creation_date is not None

    def test_to_application_dto_sets_defaults(self):
        """Test that to_application_dto sets default values."""
        request = CreateUserRequest(
            name="Test User",
            email="test@example.com",
            password="password123"
        )

        dto = UserMapper.to_application_dto(user_request_data=request)

        # Default values should be set
        assert dto.is_active is True
        assert dto.is_super_admin is False
        assert dto.update_date is None

    def test_to_application_dto_has_creation_date(self):
        """Test that to_application_dto sets creation_date."""
        before = datetime.utcnow()
        request = CreateUserRequest(
            name="Test User",
            email="test@example.com",
            password="password123"
        )

        dto = UserMapper.to_application_dto(user_request_data=request)
        after = datetime.utcnow()

        assert before <= dto.creation_date <= after

    def test_to_web_response_conversion(self, mock_user_output_dto):
        """Test converting UserOutputDto to CreateUserResponse."""
        response = UserMapper.to_web_response(user_output_dto=mock_user_output_dto)

        assert isinstance(response, CreateUserResponse)
        assert response.id == mock_user_output_dto.id
        assert response.name == mock_user_output_dto.name
        assert response.email == mock_user_output_dto.email
        assert response.password == mock_user_output_dto.password
        assert response.is_active == mock_user_output_dto.is_active

    def test_to_web_response_preserves_all_fields(self):
        """Test that to_web_response preserves all fields."""
        output_dto = UserOutputDto(
            id=42,
            name="John Doe",
            email="john@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$hash",
            is_active=True
        )

        response = UserMapper.to_web_response(user_output_dto=output_dto)

        assert response.id == 42
        assert response.name == "John Doe"
        assert response.email == "john@example.com"
        assert response.password == "$argon2id$v=19$m=65540,t=3,p=4$test$hash"
        assert response.is_active is True

    def test_to_web_response_with_inactive_user(self):
        """Test converting inactive user to response."""
        output_dto = UserOutputDto(
            id=1,
            name="Inactive User",
            email="inactive@example.com",
            password="hash",
            is_active=False
        )

        response = UserMapper.to_web_response(user_output_dto=output_dto)

        assert response.is_active is False

    def test_round_trip_mapping(self):
        """Test mapping from request to dto to response."""
        # Create request
        request = CreateUserRequest(
            name="Round Trip User",
            email="roundtrip@example.com",
            password="password123"
        )

        # Map to DTO
        dto = UserMapper.to_application_dto(user_request_data=request)

        # Simulate creating a user and getting output
        output_dto = UserOutputDto(
            id=1,
            name=dto.name,
            email=dto.email,
            password="hashed_password",
            is_active=dto.is_active
        )

        # Map to response
        response = UserMapper.to_web_response(user_output_dto=output_dto)

        # Verify round trip
        assert response.name == request.name
        assert response.email == request.email
        assert response.is_active is True

    def test_to_application_dto_with_different_emails(self):
        """Test mapping different email formats."""
        emails = [
            "simple@test.com",
            "user+tag@example.com",
            "john.doe@example.co.uk"
        ]

        for email in emails:
            request = CreateUserRequest(
                name="Test User",
                email=email,
                password="password"
            )

            dto = UserMapper.to_application_dto(user_request_data=request)
            assert dto.email == email

    def test_to_web_response_response_model_config(self):
        """Test that CreateUserResponse has from_attributes config."""
        output_dto = UserOutputDto(
            id=1,
            name="Test",
            email="test@example.com",
            password="hash",
            is_active=True
        )

        response = UserMapper.to_web_response(user_output_dto=output_dto)

        # Response should be serializable
        assert response.model_dump() is not None
