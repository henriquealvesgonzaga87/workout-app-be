import pytest
from pydantic import ValidationError

from app.application.user.dtos.user_dtos import UserOutputDto


class TestUserOutputDtoGetById:
    """Test suite for UserOutputDto used in 'get user by id' response."""

    def test_user_output_dto_initialization(self):
        """Test that UserOutputDto initializes with all required fields."""
        dto = UserOutputDto(
            id=1,
            name="Test User",
            email="test@example.com",
            password="$argon2id$v=19$m=65540,t=3,p=4$test$test123",
            is_active=True
        )
        assert dto.id == 1
        assert dto.name == "Test User"

    def test_user_output_dto_requires_id(self):
        """Test that UserOutputDto requires id field."""
        with pytest.raises(ValidationError):
            UserOutputDto(
                name="Test User",
                email="test@example.com",
                password="password123",
                is_active=True
            )

    def test_user_output_dto_requires_name(self):
        """Test that UserOutputDto requires name field."""
        with pytest.raises(ValidationError):
            UserOutputDto(
                id=1,
                email="test@example.com",
                password="password123",
                is_active=True
            )

    def test_user_output_dto_requires_email(self):
        """Test that UserOutputDto requires email field."""
        with pytest.raises(ValidationError):
            UserOutputDto(
                id=1,
                name="Test User",
                password="password123",
                is_active=True
            )

    def test_user_output_dto_requires_password(self):
        """Test that UserOutputDto requires password field."""
        with pytest.raises(ValidationError):
            UserOutputDto(
                id=1,
                name="Test User",
                email="test@example.com",
                is_active=True
            )

    def test_user_output_dto_requires_is_active(self):
        """Test that UserOutputDto requires is_active field."""
        with pytest.raises(ValidationError):
            UserOutputDto(
                id=1,
                name="Test User",
                email="test@example.com",
                password="password123"
            )

    def test_user_output_dto_email_validation_valid_format(self):
        """Test that UserOutputDto validates email format correctly."""
        dto = UserOutputDto(
            id=1,
            name="Test User",
            email="valid@example.com",
            password="password123",
            is_active=True
        )
        assert dto.email == "valid@example.com"

    def test_user_output_dto_email_validation_invalid_format(self):
        """Test that UserOutputDto rejects invalid email format."""
        with pytest.raises(ValidationError):
            UserOutputDto(
                id=1,
                name="Test User",
                email="not-an-email",
                password="password123",
                is_active=True
            )

    def test_user_output_dto_from_attributes_config(self, mock_user_schema):
        """Test that UserOutputDto can be created from ORM object."""
        dto = UserOutputDto.model_validate(mock_user_schema)
        assert dto.id == mock_user_schema.id
        assert dto.name == mock_user_schema.name
        assert dto.email == mock_user_schema.email
        assert dto.is_active == mock_user_schema.is_active

    def test_user_output_dto_with_unicode_name(self):
        """Test UserOutputDto with unicode characters."""
        dto = UserOutputDto(
            id=1,
            name="João Silva 中文",
            email="unicode@example.com",
            password="password123",
            is_active=True
        )
        assert dto.name == "João Silva 中文"

    def test_user_output_dto_is_active_true(self):
        """Test UserOutputDto with is_active=True."""
        dto = UserOutputDto(
            id=1,
            name="Active User",
            email="active@example.com",
            password="password123",
            is_active=True
        )
        assert dto.is_active is True

    def test_user_output_dto_is_active_false(self):
        """Test UserOutputDto with is_active=False."""
        dto = UserOutputDto(
            id=1,
            name="Inactive User",
            email="inactive@example.com",
            password="password123",
            is_active=False
        )
        assert dto.is_active is False

    def test_user_output_dto_preserves_password_hash(self):
        """Test that UserOutputDto preserves hashed password."""
        hash_value = "$argon2id$v=19$m=65540,t=3,p=4$test$test123"
        dto = UserOutputDto(
            id=1,
            name="Test User",
            email="test@example.com",
            password=hash_value,
            is_active=True
        )
        assert dto.password == hash_value

    def test_user_output_dto_model_validation(self, mock_user_entity):
        """Test UserOutputDto validates correctly from domain entity."""
        dto = UserOutputDto(
            id=mock_user_entity.id,
            name=mock_user_entity.name,
            email=mock_user_entity.email,
            password=mock_user_entity.password,
            is_active=mock_user_entity.is_active
        )
        assert dto.id == mock_user_entity.id
        assert dto.email == mock_user_entity.email

    def test_user_output_dto_serialization(self):
        """Test that UserOutputDto can be serialized to JSON."""
        dto = UserOutputDto(
            id=1,
            name="Test User",
            email="test@example.com",
            password="password123",
            is_active=True
        )
        serialized = dto.model_dump_json()
        assert serialized is not None
        assert '"id":1' in serialized
        assert '"name":"Test User"' in serialized
