
from datetime import datetime

from app.application.user.dtos.user_dtos import UserOutputDto
from app.presentation.mappers.user.mappers import UserMapper
from app.presentation.models.user.create_user_model import CreateUserResponse


class TestGetUserByIdMappers:
    """Test suite for UserMapper.to_web_response() for single user - Presentation layer."""

    def test_map_single_user_output_dto_to_response(self, mock_user_output_dto):
        """Test mapping single UserOutputDto to CreateUserResponse."""
        response = UserMapper.to_web_response(mock_user_output_dto)

        assert isinstance(response, CreateUserResponse)
        assert response.id == mock_user_output_dto.id
        assert response.name == mock_user_output_dto.name

    def test_map_preserves_user_id(self, mock_user_output_dto):
        """Test that mapper preserves user ID."""
        response = UserMapper.to_web_response(mock_user_output_dto)

        assert response.id == 1
        assert response.id == mock_user_output_dto.id

    def test_map_preserves_user_name(self, mock_user_output_dto):
        """Test that mapper preserves user name."""
        response = UserMapper.to_web_response(mock_user_output_dto)

        assert response.name == "Test User"
        assert response.name == mock_user_output_dto.name

    def test_map_preserves_user_email(self, mock_user_output_dto):
        """Test that mapper preserves user email."""
        response = UserMapper.to_web_response(mock_user_output_dto)

        assert response.email == mock_user_output_dto.email
        assert response.email == "test@example.com"

    def test_map_preserves_user_password(self, mock_user_output_dto):
        """Test that mapper preserves user password hash."""
        response = UserMapper.to_web_response(mock_user_output_dto)

        assert response.password == mock_user_output_dto.password
        assert "$argon2id$" in response.password

    def test_map_preserves_user_is_active(self, mock_user_output_dto):
        """Test that mapper preserves user is_active status."""
        response = UserMapper.to_web_response(mock_user_output_dto)

        assert response.is_active == mock_user_output_dto.is_active
        assert response.is_active is True

    def test_map_response_model_type(self, mock_user_output_dto):
        """Test that mapped response is CreateUserResponse model."""
        response = UserMapper.to_web_response(mock_user_output_dto)

        assert isinstance(response, CreateUserResponse)
        assert hasattr(response, 'id')
        assert hasattr(response, 'name')
        assert hasattr(response, 'email')
        assert hasattr(response, 'password')
        assert hasattr(response, 'is_active')

    def test_map_with_active_user(self):
        """Test mapping an active user."""
        active_user = UserOutputDto(
            id=5,
            name="Active User",
            email="active@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$active123",
            is_active=True,
            creation_date=datetime(2026, 4, 1, 10, 0, 0)
        )
        response = UserMapper.to_web_response(active_user)

        assert response.is_active is True
        assert response.id == 5

    def test_map_with_inactive_user(self):
        """Test mapping an inactive user."""
        inactive_user = UserOutputDto(
            id=10,
            name="Inactive User",
            email="inactive@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$inactive123",
            is_active=False,
            creation_date=datetime(2026, 4, 1, 10, 0, 0)
        )
        response = UserMapper.to_web_response(inactive_user)

        assert response.is_active is False
        assert response.id == 10

    def test_map_with_unicode_name(self):
        """Test mapping user with unicode name."""
        unicode_user = UserOutputDto(
            id=15,
            name="João Silva 中文",
            email="unicode@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$unicode123",
            is_active=True,
            creation_date=datetime(2026, 4, 1, 10, 0, 0)
        )
        response = UserMapper.to_web_response(unicode_user)

        assert response.name == "João Silva 中文"

    def test_map_with_special_characters_in_email(self):
        """Test mapping user with special characters in email."""
        special_email_user = UserOutputDto(
            id=20,
            name="Special Email User",
            email="first.last+tag@example.co.uk",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$special123",
            is_active=True,
            creation_date=datetime(2026, 4, 1, 10, 0, 0)
        )
        response = UserMapper.to_web_response(special_email_user)

        assert response.email == "first.last+tag@example.co.uk"

    def test_map_response_is_serializable(self, mock_user_output_dto):
        """Test that mapped response can be serialized."""
        response = UserMapper.to_web_response(mock_user_output_dto)

        # Should be able to convert to dict
        response_dict = response.model_dump() if hasattr(response, 'model_dump') else response.__dict__
        assert response_dict is not None
        assert 'id' in response_dict
        assert 'name' in response_dict

    def test_map_creates_new_response_object(self, mock_user_output_dto):
        """Test that mapper creates new response object (not referencing original)."""
        response = UserMapper.to_web_response(mock_user_output_dto)

        # Response should be independent object
        assert response is not mock_user_output_dto
        assert type(response) != type(mock_user_output_dto)

    def test_map_response_model_has_correct_config(self, mock_user_output_dto):
        """Test that response model has correct Pydantic config."""
        response = UserMapper.to_web_response(mock_user_output_dto)

        # Should have model config methods
        assert hasattr(response.__class__, 'model_validate') or hasattr(response.__class__, 'parse_obj')

    def test_map_with_long_name(self):
        """Test mapping user with very long name."""
        long_name = "User" * 50  # 200 character name
        long_name_user = UserOutputDto(
            id=25,
            name=long_name,
            email="longname@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$long123",
            is_active=True,
            creation_date=datetime(2026, 4, 1, 10, 0, 0)
        )
        response = UserMapper.to_web_response(long_name_user)

        assert response.name == long_name
        assert len(response.name) == 200

    def test_map_with_different_user_entities(self):
        """Test mapping multiple different user DTOs."""
        user1 = UserOutputDto(
            id=1,
            name="User One",
            email="one@example.com",
            password="$argon2hash1$",
            is_active=True,
            creation_date=datetime(2026, 4, 1, 10, 0, 0)
        )
        user2 = UserOutputDto(
            id=2,
            name="User Two",
            email="two@example.com",
            password="$argon2hash2$",
            is_active=False,
            creation_date=datetime(2026, 4, 1, 10, 0, 0)
        )

        response1 = UserMapper.to_web_response(user1)
        response2 = UserMapper.to_web_response(user2)

        assert response1.id != response2.id
        assert response1.name != response2.name
        assert response1.is_active != response2.is_active
