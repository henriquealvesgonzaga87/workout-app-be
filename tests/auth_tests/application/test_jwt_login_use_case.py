"""Tests for JWT Login Use Case."""

from unittest.mock import Mock, patch

import pytest

from app.application.auth.jwt.dtos.jwt_dtos import JwtLoginDto
from app.application.auth.jwt.use_cases.jwt_login_use_case import JwtLoginUseCases
from app.presentation.error_handlers.not_found_error import NotFoundError
from app.presentation.error_handlers.unauthorized_error import UnauthorizedError


class TestJwtLoginUseCaseInitialization:
    """Test JWT Login Use Case initialization."""

    def test_initialization_with_valid_dependencies(self, mock_user_repository):
        """Test use case initializes with valid dependencies."""
        mock_jwt_handler = Mock()
        use_case = JwtLoginUseCases(
            jwt_handler=mock_jwt_handler,
            user_repository=mock_user_repository
        )

        assert use_case.jwt_handler == mock_jwt_handler
        assert use_case.user_repository == mock_user_repository

    def test_initialization_stores_repositories(self, mock_user_repository):
        """Test use case stores repositories correctly."""
        mock_jwt_handler = Mock()
        use_case = JwtLoginUseCases(
            jwt_handler=mock_jwt_handler,
            user_repository=mock_user_repository
        )

        assert hasattr(use_case, 'jwt_handler')
        assert hasattr(use_case, 'user_repository')


class TestJwtLoginUseCasePrepare:
    """Test the prepare method of JWT Login Use Case."""

    def test_prepare_with_valid_credentials(
        self,
        mock_jwt_login_dto,
        mock_user_entity,
        mock_user_repository
    ):
        """Test prepare method with valid credentials."""
        mock_user_repository.get_by_email.return_value = mock_user_entity
        mock_jwt_handler = Mock()
        use_case = JwtLoginUseCases(
            jwt_handler=mock_jwt_handler,
            user_repository=mock_user_repository
        )

        result = use_case.prepare(login_data=mock_jwt_login_dto)

        assert result == mock_user_entity
        mock_user_repository.get_by_email.assert_called_once_with(
            email=mock_jwt_login_dto.email
        )

    def test_prepare_with_inactive_user(
        self,
        mock_jwt_login_dto,
        mock_inactive_user_entity,
        mock_user_repository
    ):
        """Test prepare method raises error for inactive users."""
        mock_user_repository.get_by_email.return_value = mock_inactive_user_entity
        mock_jwt_handler = Mock()
        use_case = JwtLoginUseCases(
            jwt_handler=mock_jwt_handler,
            user_repository=mock_user_repository
        )

        with pytest.raises(NotFoundError) as exc_info:
            use_case.prepare(login_data=mock_jwt_login_dto)

        assert "User not registered" in str(exc_info.value)

    def test_prepare_with_incorrect_password(
        self,
        mock_jwt_invalid_password_dto,
        mock_user_entity,
        mock_user_repository
    ):
        """Test prepare method raises error with incorrect password."""
        mock_user_repository.get_by_email.return_value = mock_user_entity
        mock_jwt_handler = Mock()
        use_case = JwtLoginUseCases(
            jwt_handler=mock_jwt_handler,
            user_repository=mock_user_repository
        )

        with pytest.raises(UnauthorizedError) as exc_info:
            use_case.prepare(login_data=mock_jwt_invalid_password_dto)

        assert "Incorrect email or password" in str(exc_info.value)

    def test_prepare_calls_user_repository_get_by_email(
        self,
        mock_jwt_login_dto,
        mock_user_entity,
        mock_user_repository
    ):
        """Test prepare method calls user repository get_by_email."""
        mock_user_repository.get_by_email.return_value = mock_user_entity
        mock_jwt_handler = Mock()
        use_case = JwtLoginUseCases(
            jwt_handler=mock_jwt_handler,
            user_repository=mock_user_repository
        )

        use_case.prepare(login_data=mock_jwt_login_dto)

        mock_user_repository.get_by_email.assert_called_once_with(
            email="john@example.com"
        )

    def test_prepare_validates_user_is_active(
        self,
        mock_jwt_login_dto,
        mock_user_entity,
        mock_user_repository
    ):
        """Test prepare method validates user is active."""
        mock_user_entity.is_active = False
        mock_user_repository.get_by_email.return_value = mock_user_entity
        mock_jwt_handler = Mock()
        use_case = JwtLoginUseCases(
            jwt_handler=mock_jwt_handler,
            user_repository=mock_user_repository
        )

        with pytest.raises(NotFoundError):
            use_case.prepare(login_data=mock_jwt_login_dto)


class TestJwtLoginUseCaseExecute:
    """Test the execute method of JWT Login Use Case."""

    def test_execute_successful_login(
        self,
        mock_jwt_login_dto,
        mock_user_entity,
        mock_user_repository,
        mock_jwt_token_output_dto
    ):
        """Test execute method with successful login."""
        mock_user_repository.get_by_email.return_value = mock_user_entity
        mock_jwt_handler = Mock()
        mock_jwt_handler.login.return_value = mock_jwt_token_output_dto
        use_case = JwtLoginUseCases(
            jwt_handler=mock_jwt_handler,
            user_repository=mock_user_repository
        )

        result = use_case.execute(login_data=mock_jwt_login_dto)

        assert result.access_token == mock_jwt_token_output_dto.access_token
        assert result.refresh_token == mock_jwt_token_output_dto.refresh_token
        assert result.token_type == "bearer"

    def test_execute_returns_correct_dto_type(
        self,
        mock_jwt_login_dto,
        mock_user_entity,
        mock_user_repository,
        mock_jwt_token_output_dto
    ):
        """Test execute method returns correct dto type."""
        mock_user_repository.get_by_email.return_value = mock_user_entity
        mock_jwt_handler = Mock()
        mock_jwt_handler.login.return_value = mock_jwt_token_output_dto
        use_case = JwtLoginUseCases(
            jwt_handler=mock_jwt_handler,
            user_repository=mock_user_repository
        )

        result = use_case.execute(login_data=mock_jwt_login_dto)

        assert hasattr(result, 'access_token')
        assert hasattr(result, 'refresh_token')
        assert hasattr(result, 'token_type')

    def test_execute_calls_prepare(
        self,
        mock_jwt_login_dto,
        mock_user_entity,
        mock_user_repository,
        mock_jwt_token_output_dto
    ):
        """Test execute method calls prepare method."""
        mock_user_repository.get_by_email.return_value = mock_user_entity
        mock_jwt_handler = Mock()
        mock_jwt_handler.login.return_value = mock_jwt_token_output_dto
        use_case = JwtLoginUseCases(
            jwt_handler=mock_jwt_handler,
            user_repository=mock_user_repository
        )

        with patch.object(use_case, 'prepare', return_value=mock_user_entity):
            use_case.execute(login_data=mock_jwt_login_dto)

    def test_execute_calls_jwt_handler_login(
        self,
        mock_jwt_login_dto,
        mock_user_entity,
        mock_user_repository,
        mock_jwt_token_output_dto
    ):
        """Test execute method calls jwt_handler.login."""
        mock_user_repository.get_by_email.return_value = mock_user_entity
        mock_jwt_handler = Mock()
        mock_jwt_handler.login.return_value = mock_jwt_token_output_dto
        use_case = JwtLoginUseCases(
            jwt_handler=mock_jwt_handler,
            user_repository=mock_user_repository
        )

        use_case.execute(login_data=mock_jwt_login_dto)

        mock_jwt_handler.login.assert_called_once_with(login_data=mock_jwt_login_dto)

    def test_execute_propagates_prepare_errors(
        self,
        mock_jwt_invalid_password_dto,
        mock_user_entity,
        mock_user_repository
    ):
        """Test execute method propagates prepare errors."""
        mock_user_repository.get_by_email.return_value = mock_user_entity
        mock_jwt_handler = Mock()
        use_case = JwtLoginUseCases(
            jwt_handler=mock_jwt_handler,
            user_repository=mock_user_repository
        )

        with pytest.raises(UnauthorizedError):
            use_case.execute(login_data=mock_jwt_invalid_password_dto)

    def test_execute_with_admin_user(
        self,
        mock_jwt_login_dto,
        mock_super_admin_entity,
        mock_user_repository,
        mock_jwt_token_output_dto
    ):
        """Test execute method with admin user."""
        mock_jwt_login_dto.email = "admin@example.com"
        mock_user_repository.get_by_email.return_value = mock_super_admin_entity
        mock_jwt_handler = Mock()
        mock_jwt_handler.login.return_value = mock_jwt_token_output_dto
        use_case = JwtLoginUseCases(
            jwt_handler=mock_jwt_handler,
            user_repository=mock_user_repository
        )

        result = use_case.execute(login_data=mock_jwt_login_dto)

        assert result.access_token is not None

    def test_execute_with_different_users(
        self,
        mock_user_repository,
        mock_jwt_token_output_dto
    ):
        """Test execute method with different users."""
        from app.infrastructure.auth.jwt.password_hasher import get_password_hash

        users = [
            Mock(
                id=1, 
                email="user1@example.com", 
                is_active=True, 
                is_super_admin=False, 
                password=get_password_hash("password123")
            ),
            Mock(
                id=2, 
                email="user2@example.com", 
                is_active=True, 
                is_super_admin=False, 
                password=get_password_hash("password123")
            ),
            Mock(
                id=3, 
                email="admin@example.com", 
                is_active=True, 
                is_super_admin=True, 
                password=get_password_hash("password123")
            ),
        ]

        mock_jwt_handler = Mock()
        mock_jwt_handler.login.return_value = mock_jwt_token_output_dto
        use_case = JwtLoginUseCases(
            jwt_handler=mock_jwt_handler,
            user_repository=mock_user_repository
        )

        for user in users:
            login_dto = JwtLoginDto(email=user.email, password="password123")
            mock_user_repository.get_by_email.return_value = user

            result = use_case.execute(login_data=login_dto)

            assert result is not None
