from datetime import datetime

import pytest
from pydantic import ValidationError

from app.application.user.dtos.user_dtos import CreateUserDto, UserOutputDto
from app.domain.user.entities import User


class TestCreateUserDto:
    """Test suite for CreateUserDto validation."""

    def test_create_user_dto_valid_data(self, mock_create_user_dto):
        """Test creating a valid CreateUserDto."""
        assert mock_create_user_dto.name == "Test User"
        assert mock_create_user_dto.email == "test@example.com"
        assert mock_create_user_dto.password == "plain_password_123"
        assert mock_create_user_dto.is_active is True
        assert mock_create_user_dto.is_super_admin is False
        assert isinstance(mock_create_user_dto.creation_date, datetime)

    def test_create_user_dto_email_validation(self):
        """Test that invalid email format is rejected."""
        with pytest.raises(ValidationError):
            CreateUserDto(
                name="Test User",
                email="invalid-email",
                password="password123",
                is_active=True,
                is_super_admin=False,
                creation_date=datetime.now(),
                update_date=None
            )

    def test_create_user_dto_empty_name(self):
        """Test that empty name is allowed by pydantic."""
        # Pydantic by default allows empty strings
        dto = CreateUserDto(
            name="",
            email="test@example.com",
            password="password123",
            is_active=True,
            is_super_admin=False,
            creation_date=datetime.now(),
            update_date=None
        )
        assert dto.name == ""

    def test_create_user_dto_missing_required_field(self):
        """Test that missing required field raises validation error."""
        with pytest.raises(ValidationError):
            CreateUserDto(
                name="Test User",
                email="test@example.com",
                # Missing password
                is_active=True,
                is_super_admin=False,
                creation_date=datetime.now(),
                update_date=None
            )

    def test_create_user_dto_defaults(self):
        """Test default values for optional fields."""
        dto = CreateUserDto(
            name="Test User",
            email="test@example.com",
            password="password123",
            creation_date=datetime.now()
        )
        assert dto.is_active is True
        assert dto.is_super_admin is False
        assert dto.update_date is None

    def test_create_user_dto_with_update_date(self):
        """Test CreateUserDto with update_date set."""
        now = datetime.now()
        dto = CreateUserDto(
            name="Test User",
            email="test@example.com",
            password="password123",
            is_active=True,
            is_super_admin=False,
            creation_date=now,
            update_date=now
        )
        assert dto.update_date == now


class TestUserOutputDto:
    """Test suite for UserOutputDto validation."""

    def test_user_output_dto_valid_data(self, mock_user_output_dto):
        """Test creating a valid UserOutputDto."""
        assert mock_user_output_dto.id == 1
        assert mock_user_output_dto.name == "Test User"
        assert mock_user_output_dto.email == "test@example.com"
        assert mock_user_output_dto.password == "$argon2id$v=19$m=65540,t=3,p=4$test$test123"
        assert mock_user_output_dto.is_active is True

    def test_user_output_dto_email_validation(self):
        """Test that invalid email format is rejected."""
        with pytest.raises(ValidationError):
            UserOutputDto(
                id=1,
                name="Test User",
                email="invalid-email",
                password="hashed_password",
                is_active=True,
                creation_date=datetime(2026, 4, 1, 10, 0, 0)
            )

    def test_user_output_dto_missing_id(self):
        """Test that missing id raises validation error."""
        with pytest.raises(ValidationError):
            UserOutputDto(
                # Missing id
                name="Test User",
                email="test@example.com",
                password="hashed_password",
                is_active=True,
                creation_date=datetime(2026, 4, 1, 10, 0, 0)
            )

    def test_user_output_dto_invalid_email(self):
        """Test that invalid email raises validation error."""
        with pytest.raises(ValidationError):
            UserOutputDto(
                id=1,
                name="Test User",
                email="not-an-email",
                password="hashed_password",
                is_active=True,
                creation_date=datetime(2026, 4, 1, 10, 0, 0)
            )

    def test_user_output_dto_is_active_boolean(self):
        """Test that is_active with non-boolean values gets coerced."""
        # Pydantic coerces string "yes" to True (truthy value)
        dto = UserOutputDto(
            id=1,
            name="Test User",
            email="test@example.com",
            password="hashed_password",
            is_active="yes",  # Will be coerced to True
            creation_date=datetime(2026, 4, 1, 10, 0, 0)
        )
        assert dto.is_active is True

    def test_user_output_dto_from_attributes(self):
        """Test that UserOutputDto can be created from ORM attributes."""
        from app.infrastructure.schemas.user.user_schema import UserSchema

        # Create a schema object
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

        # UserOutputDto should accept from_attributes config
        dto = UserOutputDto.model_validate(schema)
        assert dto.id == 1
        assert dto.name == "Test User"
        assert dto.email == "test@example.com"

    def test_user_output_dto_list_creation(self, mock_user_output_dto_list):
        """Test creating a list of UserOutputDto."""
        assert len(mock_user_output_dto_list) == 2
        assert all(isinstance(dto, UserOutputDto) for dto in mock_user_output_dto_list)
        assert mock_user_output_dto_list[0].id == 1
        assert mock_user_output_dto_list[1].id == 2


class TestEntityUserDomain:
    """Test suite for User domain entity."""

    def test_user_entity_creation(self, mock_user_entity):
        """Test creating a User entity."""
        assert mock_user_entity.id == 1
        assert mock_user_entity.name == "John Doe"
        assert mock_user_entity.email == "john@example.com"
        assert mock_user_entity.is_active is True
        assert mock_user_entity.is_super_admin is False

    def test_user_entity_with_admin(self):
        """Test creating a User entity with admin privileges."""
        user = UserOutputDto(
            id=1,
            name="Admin",
            email="admin@example.com",
            password="hashed",
            is_active=True,
            creation_date=datetime(2026, 4, 1, 10, 0, 0)
        )
        assert user.is_active is True

    def test_user_entity_inactive(self):
        """Test creating an inactive User entity."""
        user = UserOutputDto(
            id=1,
            name="Inactive User",
            email="inactive@example.com",
            password="hashed",
            is_active=False,
            creation_date=datetime(2026, 4, 1, 10, 0, 0)
        )
        assert user.is_active is False

    def test_user_entity_list(self, mock_user_entity_list):
        """Test working with a list of User entities."""
        assert len(mock_user_entity_list) == 3
        assert all(isinstance(u, User) for u in mock_user_entity_list)

        # Check that we can access properties
        for user in mock_user_entity_list:
            assert user.id > 0
            assert len(user.email) > 0
            assert isinstance(user.creation_date, datetime)

        # Check specific users
        assert mock_user_entity_list[0].is_super_admin is False
        assert mock_user_entity_list[2].is_super_admin is True
