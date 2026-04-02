import pytest

from app.application.user.dtos.user_dtos import UserOutputDto
from app.application.user.use_cases.get_user_by_id_use_case import GetUserByIdUseCase
from app.presentation.error_handlers.request_error import RequestError


class TestGetUserByIdUseCase:
    """Test suite for GetUserByIdUseCase - Application layer for 'get user by id'."""

    def test_get_user_by_id_use_case_initialization(self, mock_user_repository):
        """Test that GetUserByIdUseCase initializes with repository."""
        use_case = GetUserByIdUseCase(user_repository=mock_user_repository)
        assert use_case.user_repositoy == mock_user_repository

    def test_prepare_with_valid_integer_id(self, mock_user_repository):
        """Test prepare method with a valid integer ID."""
        use_case = GetUserByIdUseCase(user_repository=mock_user_repository)
        result = use_case.prepare(id=1)
        assert result == 1
        assert isinstance(result, int)

    def test_prepare_with_string_integer_id(self, mock_user_repository):
        """Test prepare method converts string ID to integer."""
        use_case = GetUserByIdUseCase(user_repository=mock_user_repository)
        result = use_case.prepare(id="42")
        assert result == 42
        assert isinstance(result, int)

    def test_prepare_with_invalid_id_raises_request_error(self, mock_user_repository):
        """Test prepare method raises RequestError with invalid ID."""
        use_case = GetUserByIdUseCase(user_repository=mock_user_repository)
        with pytest.raises(RequestError):
            use_case.prepare(id="invalid_id")

    def test_prepare_with_float_id_converts_to_int(self, mock_user_repository):
        """Test prepare method converts float ID to integer."""
        use_case = GetUserByIdUseCase(user_repository=mock_user_repository)
        result = use_case.prepare(id=3.14)
        assert result == 3
        assert isinstance(result, int)

    def test_execute_returns_user_output_dto(self, mock_user_repository, mock_user_entity):
        """Test that execute returns a UserOutputDto."""
        mock_user_repository.get_by_id.return_value = mock_user_entity

        use_case = GetUserByIdUseCase(user_repository=mock_user_repository)
        result = use_case.execute(id=1)

        assert isinstance(result, UserOutputDto)
        assert result.id == 1
        assert result.name == "John Doe"

    def test_execute_with_specific_user_id(self, mock_user_repository, mock_user_entity):
        """Test execute returns correct user for given ID."""
        mock_user_repository.get_by_id.return_value = mock_user_entity

        use_case = GetUserByIdUseCase(user_repository=mock_user_repository)
        result = use_case.execute(id=1)

        mock_user_repository.get_by_id.assert_called_once_with(id=1)
        assert result.id == 1
        assert result.name == "John Doe"
        assert result.email == "john@example.com"

    def test_execute_calls_prepare_before_repository(self, mock_user_repository, mock_user_entity):
        """Test that execute calls prepare method to validate ID."""
        mock_user_repository.get_by_id.return_value = mock_user_entity

        use_case = GetUserByIdUseCase(user_repository=mock_user_repository)
        result = use_case.execute(id="1")

        # prepare should convert string to int
        mock_user_repository.get_by_id.assert_called_once()
        assert isinstance(result, UserOutputDto)

    def test_execute_preserves_all_user_fields(self, mock_user_repository, mock_user_entity):
        """Test that execute preserves all user fields in UserOutputDto."""
        mock_user_repository.get_by_id.return_value = mock_user_entity

        use_case = GetUserByIdUseCase(user_repository=mock_user_repository)
        result = use_case.execute(id=1)

        assert result.id == mock_user_entity.id
        assert result.name == mock_user_entity.name
        assert result.email == mock_user_entity.email
        assert result.password == mock_user_entity.password
        assert result.is_active == mock_user_entity.is_active

    def test_execute_with_inactive_user(self, mock_user_repository):
        """Test execute with an inactive user."""
        from datetime import datetime

        from app.domain.user.entities import User

        inactive_user = User(
            id=5,
            name="Inactive User",
            email="inactive@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$test123",
            is_active=False,
            is_super_admin=False,
            creation_date=datetime(2026, 4, 1, 10, 0, 0),
            update_date=None
        )
        mock_user_repository.get_by_id.return_value = inactive_user

        use_case = GetUserByIdUseCase(user_repository=mock_user_repository)
        result = use_case.execute(id=5)

        assert result.is_active is False
        assert result.id == 5

    def test_execute_with_admin_user(self, mock_user_repository):
        """Test execute with an admin (super_admin) user."""
        from datetime import datetime

        from app.domain.user.entities import User

        admin_user = User(
            id=10,
            name="Admin User",
            email="admin@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$admin123",
            is_active=True,
            is_super_admin=True,
            creation_date=datetime(2026, 4, 1, 10, 0, 0),
            update_date=None
        )
        mock_user_repository.get_by_id.return_value = admin_user

        use_case = GetUserByIdUseCase(user_repository=mock_user_repository)
        result = use_case.execute(id=10)

        assert result.id == 10
        assert result.name == "Admin User"

    def test_execute_with_unicode_name(self, mock_user_repository):
        """Test execute with unicode characters in user name."""
        from datetime import datetime

        from app.domain.user.entities import User

        unicode_user = User(
            id=15,
            name="João Silva 中文",
            email="unicode@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$unicode123",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime(2026, 4, 1, 10, 0, 0),
            update_date=None
        )
        mock_user_repository.get_by_id.return_value = unicode_user

        use_case = GetUserByIdUseCase(user_repository=mock_user_repository)
        result = use_case.execute(id=15)

        assert result.name == "João Silva 中文"
        assert isinstance(result, UserOutputDto)
