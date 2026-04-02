
import pytest

from app.application.user.dtos.user_dtos import UserOutputDto
from app.application.user.use_cases.get_all_users_use_case import GetAllUsersUseCase
from app.presentation.error_handlers.reponse_error import ResponseError


class TestGetAllUsersUseCase:
    """Test suite for GetAllUsersUseCase - Application layer for 'get users'."""

    def test_get_all_users_use_case_initialization(self, mock_user_repository):
        """Test that GetAllUsersUseCase initializes with repository."""
        use_case = GetAllUsersUseCase(user_repository=mock_user_repository)
        assert use_case.user_repository == mock_user_repository

    def test_prepare_method_does_nothing(self, mock_user_repository):
        """Test that prepare method exists and does nothing."""
        use_case = GetAllUsersUseCase(user_repository=mock_user_repository)
        result = use_case.prepare()
        assert result is None

    def test_execute_returns_list_of_user_output_dtos(self, mock_user_repository, mock_user_entity_list):
        """Test that execute returns a list of UserOutputDto."""
        mock_user_repository.get_users.return_value = mock_user_entity_list

        use_case = GetAllUsersUseCase(user_repository=mock_user_repository)
        result = use_case.execute()

        assert isinstance(result, list)
        assert len(result) == 3
        assert all(isinstance(user, UserOutputDto) for user in result)

    def test_execute_with_single_user(self, mock_user_repository, mock_user_entity):
        """Test execute with a single user from repository."""
        mock_user_repository.get_users.return_value = [mock_user_entity]

        use_case = GetAllUsersUseCase(user_repository=mock_user_repository)
        result = use_case.execute()

        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], UserOutputDto)
        assert result[0].id == 1
        assert result[0].name == "John Doe"

    def test_execute_with_empty_user_list(self, mock_user_repository):
        """Test execute with empty user list from repository."""
        mock_user_repository.get_users.return_value = []

        use_case = GetAllUsersUseCase(user_repository=mock_user_repository)
        result = use_case.execute()

        assert isinstance(result, list)
        assert len(result) == 0

    def test_execute_validates_users_with_dto(self, mock_user_repository, mock_user_entity_list):
        """Test that execute validates each user using UserOutputDto."""
        mock_user_repository.get_users.return_value = mock_user_entity_list

        use_case = GetAllUsersUseCase(user_repository=mock_user_repository)
        result = use_case.execute()

        # Verify each user has all required DTO fields
        for user in result:
            assert hasattr(user, 'id')
            assert hasattr(user, 'name')
            assert hasattr(user, 'email')
            assert hasattr(user, 'password')
            assert hasattr(user, 'is_active')

    def test_execute_preserves_user_order(self, mock_user_repository):
        """Test that execute preserves the order of users from repository."""
        from datetime import datetime

        from app.domain.user.entities import User

        users = [
            User(
                id=3, 
                name="User C", 
                email="c@example.com", 
                password="hash", 
                is_active=True, 
                is_super_admin=False, 
                creation_date=datetime.now(), 
                update_date=None
            ),
            User(
                id=1, 
                name="User A", 
                email="a@example.com", 
                password="hash", 
                is_active=True, 
                is_super_admin=False, 
                creation_date=datetime.now(), 
                update_date=None
            ),
            User(
                id=2, 
                name="User B", 
                email="b@example.com", 
                password="hash", 
                is_active=True, 
                is_super_admin=False, 
                creation_date=datetime.now(), 
                update_date=None
            ),
        ]
        mock_user_repository.get_users.return_value = users

        use_case = GetAllUsersUseCase(user_repository=mock_user_repository)
        result = use_case.execute()

        # Order should be preserved as returned from repository
        assert result[0].id == 3
        assert result[1].id == 1
        assert result[2].id == 2

    def test_execute_calls_repository_get_users(self, mock_user_repository, mock_user_entity_list):
        """Test that execute calls repository.get_users()."""
        mock_user_repository.get_users.return_value = mock_user_entity_list

        use_case = GetAllUsersUseCase(user_repository=mock_user_repository)
        use_case.execute()

        # Verify repository method was called
        mock_user_repository.get_users.assert_called_once()

    def test_execute_with_validation_error(self, mock_user_repository):
        """Test that validation errors are wrapped in ResponseError."""
        # Return data that can't be validated as UserOutputDto
        mock_user_repository.get_users.return_value = [
            {"invalid": "data"}  # Missing required fields
        ]

        use_case = GetAllUsersUseCase(user_repository=mock_user_repository)

        with pytest.raises(ResponseError):
            use_case.execute()

    def test_execute_returns_correct_user_data(self, mock_user_repository, mock_user_entity_list):
        """Test that execute returns users with correct data mapping."""
        mock_user_repository.get_users.return_value = mock_user_entity_list

        use_case = GetAllUsersUseCase(user_repository=mock_user_repository)
        result = use_case.execute()

        # Verify first user
        assert result[0].name == "John Doe"
        assert result[0].email == "john@example.com"
        assert result[0].is_active is True

        # Verify second user
        assert result[1].name == "Jane Smith"
        assert result[1].email == "jane@example.com"

        # Verify admin user
        assert result[2].name == "Admin User"

    def test_execute_with_inactive_users(self, mock_user_repository):
        """Test execute handles inactive users correctly."""
        from datetime import datetime

        from app.domain.user.entities import User

        users = [
            User(
                id=1,
                name="Active", 
                email="active@example.com", 
                password="hash", is_active=True, 
                is_super_admin=False, 
                creation_date=datetime.now(), 
                update_date=None
            ),
            User(
                id=2, 
                name="Inactive", 
                email="inactive@example.com", 
                password="hash", 
                is_active=False, 
                is_super_admin=False, 
                creation_date=datetime.now(),
                  update_date=None
            ),
        ]
        mock_user_repository.get_users.return_value = users

        use_case = GetAllUsersUseCase(user_repository=mock_user_repository)
        result = use_case.execute()

        assert result[0].is_active is True
        assert result[1].is_active is False
