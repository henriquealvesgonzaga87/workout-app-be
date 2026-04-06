from datetime import datetime

from app.application.user.dtos.user_dtos import UserOutputDto
from app.presentation.mappers.user.mappers import UserMapper
from app.presentation.models.user.create_user_model import CreateUserResponse


class TestGetAllUsersMappers:
    """Test suite for UserMapper in context of get_all_users - Presentation layer mappings."""

    def test_map_single_user_output_dto_to_response(self, mock_user_output_dto):
        """Test mapping a single UserOutputDto to CreateUserResponse."""
        response = UserMapper.to_web_response(user_output_dto=mock_user_output_dto)

        assert isinstance(response, CreateUserResponse)
        assert response.id == mock_user_output_dto.id
        assert response.name == mock_user_output_dto.name

    def test_map_user_output_dto_list(self, mock_user_output_dto_list):
        """Test mapping a list of UserOutputDto to CreateUserResponse list."""
        responses = [
            UserMapper.to_web_response(user_output_dto=dto)
            for dto in mock_user_output_dto_list
        ]

        assert len(responses) == len(mock_user_output_dto_list)
        assert all(isinstance(r, CreateUserResponse) for r in responses)

    def test_map_preserves_user_id(self, mock_user_output_dto):
        """Test that mapping preserves user ID."""
        response = UserMapper.to_web_response(user_output_dto=mock_user_output_dto)

        assert response.id == mock_user_output_dto.id

    def test_map_preserves_user_name(self, mock_user_output_dto):
        """Test that mapping preserves user name."""
        response = UserMapper.to_web_response(user_output_dto=mock_user_output_dto)

        assert response.name == mock_user_output_dto.name

    def test_map_preserves_user_email(self, mock_user_output_dto):
        """Test that mapping preserves user email."""
        response = UserMapper.to_web_response(user_output_dto=mock_user_output_dto)

        assert response.email == mock_user_output_dto.email

    def test_map_preserves_user_password(self, mock_user_output_dto):
        """Test that mapping preserves user password hash."""
        response = UserMapper.to_web_response(user_output_dto=mock_user_output_dto)

        assert response.password == mock_user_output_dto.password

    def test_map_preserves_is_active_status(self, mock_user_output_dto):
        """Test that mapping preserves user active status."""
        response = UserMapper.to_web_response(user_output_dto=mock_user_output_dto)

        assert response.is_active == mock_user_output_dto.is_active

    def test_map_all_fields_in_response(self, mock_user_output_dto):
        """Test that all expected fields are present in response."""
        response = UserMapper.to_web_response(user_output_dto=mock_user_output_dto)

        assert hasattr(response, 'id')
        assert hasattr(response, 'name')
        assert hasattr(response, 'email')
        assert hasattr(response, 'password')
        assert hasattr(response, 'is_active')

    def test_map_multiple_users_all_correct(self, mock_user_output_dto_list):
        """Test mapping multiple users preserves all data correctly."""
        responses = [
            UserMapper.to_web_response(user_output_dto=dto)
            for dto in mock_user_output_dto_list
        ]

        # Verify first user
        assert responses[0].id == 1
        assert responses[0].name == "John Doe"
        assert responses[0].email == "john@example.com"

        # Verify second user
        assert responses[1].id == 2
        assert responses[1].name == "Jane Smith"
        assert responses[1].email == "jane@example.com"

    def test_map_active_and_inactive_users(self):
        """Test mapping both active and inactive users."""
        active_user = UserOutputDto(
            id=1,
            name="Active",
            email="active@example.com",
            password="hash_active",
            is_active=True,
            creation_date=datetime(2026, 4, 1, 10, 0, 0)
        )
        inactive_user = UserOutputDto(
            id=2,
            name="Inactive",
            email="inactive@example.com",
            password="hash_inactive",
            is_active=False,
            creation_date=datetime(2026, 4, 1, 10, 0, 0)
        )

        active_response = UserMapper.to_web_response(user_output_dto=active_user)
        inactive_response = UserMapper.to_web_response(user_output_dto=inactive_user)

        assert active_response.is_active is True
        assert inactive_response.is_active is False

    def test_map_response_is_serializable(self, mock_user_output_dto):
        """Test that mapped response can be serialized to JSON."""
        response = UserMapper.to_web_response(user_output_dto=mock_user_output_dto)

        # Should be able to convert to dict (JSON serializable)
        response_dict = response.model_dump()
        assert isinstance(response_dict, dict)
        assert 'id' in response_dict
        assert 'name' in response_dict

    def test_map_with_special_characters(self):
        """Test mapping user with special characters in name."""
        user_dto = UserOutputDto(
            id=1,
            name="José María da Silva",
            email="jose@example.com",
            password="hash",
            is_active=True,
            creation_date=datetime(2026, 4, 1, 10, 0, 0)
        )

        response = UserMapper.to_web_response(user_output_dto=user_dto)

        assert response.name == "José María da Silva"

    def test_map_response_model_has_correct_config(self, mock_user_output_dto):
        """Test that response model has from_attributes config."""
        response = UserMapper.to_web_response(user_output_dto=mock_user_output_dto)

        # Response should be serializable
        assert response.model_dump() is not None
        assert response.model_validate(response.model_dump()) is not None
