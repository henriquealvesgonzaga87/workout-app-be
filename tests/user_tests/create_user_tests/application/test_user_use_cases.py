from datetime import datetime
from unittest.mock import Mock

import pytest
from pydantic import ValidationError

from app.application.user.dtos.user_dtos import CreateUserDto, UserOutputDto
from app.application.user.use_cases.create_user_use_case import (
    CreateUserUseCase,
)
from app.domain.user.entities import User
from app.presentation.error_handlers.reponse_error import ResponseError


class TestCreateUserUseCase:
    """Test suite for CreateUserUseCase."""

    def test_create_user_use_case_initialization(self, mock_user_repository):
        """Test that use case initializes correctly."""
        use_case = CreateUserUseCase(user_repository=mock_user_repository)
        assert use_case.user_repository == mock_user_repository

    def test_prepare_method_hashes_password(self, mock_create_user_dto):
        """Test that prepare method hashes the password."""
        mock_repo = Mock()
        use_case = CreateUserUseCase(user_repository=mock_repo)

        prepared_dto = use_case.prepare(user_dto=mock_create_user_dto)

        # Password should be hashed and different from original
        assert prepared_dto.password != mock_create_user_dto.password
        assert len(prepared_dto.password) > len(mock_create_user_dto.password)
        # Other fields should remain the same
        assert prepared_dto.name == mock_create_user_dto.name
        assert prepared_dto.email == mock_create_user_dto.email

    def test_prepare_method_preserves_user_data(self, mock_create_user_dto):
        """Test that prepare method preserves user data."""
        mock_repo = Mock()
        use_case = CreateUserUseCase(user_repository=mock_repo)

        prepared_dto = use_case.prepare(user_dto=mock_create_user_dto)

        assert prepared_dto.name == mock_create_user_dto.name
        assert prepared_dto.email == mock_create_user_dto.email
        assert prepared_dto.is_active == mock_create_user_dto.is_active
        assert prepared_dto.is_super_admin == mock_create_user_dto.is_super_admin

    def test_execute_creates_user_successfully(self, mock_user_repository, mock_create_user_dto, mock_user_entity):
        """Test successful user creation."""
        mock_user_repository.create.return_value = mock_user_entity

        use_case = CreateUserUseCase(user_repository=mock_user_repository)
        result = use_case.execute(user_dto=mock_create_user_dto)

        assert isinstance(result, UserOutputDto)
        assert result.name == mock_user_entity.name
        assert result.email == mock_user_entity.email
        assert result.id == mock_user_entity.id
        mock_user_repository.create.assert_called_once()

    def test_execute_returns_user_output_dto(self, mock_user_repository, mock_create_user_dto):
        """Test that execute returns UserOutputDto."""
        mock_user = User(
            id=42,
            name="Test User",
            email="test@example.com",
            password="hashed",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime.now(),
            update_date=None
        )
        mock_user_repository.create.return_value = mock_user

        use_case = CreateUserUseCase(user_repository=mock_user_repository)
        result = use_case.execute(user_dto=mock_create_user_dto)

        assert isinstance(result, UserOutputDto)
        assert result.id == 42
        assert result.name == "Test User"
        assert result.email == "test@example.com"

    def test_execute_with_validation_error(self, mock_user_repository):
        """Test that validation error in execute is wrapped in ResponseError."""
        # Create a user that will fail validation at repository level
        valid_dto = CreateUserDto(
            name="Test",
            email="test@example.com",
            password="password",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime.now()
        )
        mock_user_repository.create.side_effect = ValidationError.from_exception_data("test", [])

        use_case = CreateUserUseCase(user_repository=mock_user_repository)

        with pytest.raises(ResponseError):
            use_case.execute(user_dto=valid_dto)

    def test_prepare_with_invalid_password(self, mock_user_repository):
        """Test prepare with None password."""
        invalid_dto = CreateUserDto(
            name="Test",
            email="test@example.com",
            password="",  # Empty password
            is_active=True,
            is_super_admin=False,
            creation_date=datetime.now()
        )

        use_case = CreateUserUseCase(user_repository=mock_user_repository)
        prepared = use_case.prepare(user_dto=invalid_dto)

        # Password should still be hashed, even if empty
        assert prepared.password != invalid_dto.password
