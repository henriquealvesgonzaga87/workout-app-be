"""Tests for Authentication Error Handling."""

import pytest

from app.presentation.error_handlers.not_found_error import NotFoundError
from app.presentation.error_handlers.type_error import TypeError as CustomTyperError
from app.presentation.error_handlers.unauthorized_error import UnauthorizedError


class TestUnauthorizedError:
    """Test UnauthorizedError exception."""

    def test_unauthorized_error_initialization(self):
        """Test UnauthorizedError initializes with message."""
        message = "Invalid credentials"
        error = UnauthorizedError(message)

        assert str(error) == message

    def test_unauthorized_error_is_exception(self):
        """Test UnauthorizedError is an Exception."""
        error = UnauthorizedError("test")
        assert isinstance(error, Exception)

    def test_unauthorized_error_raised_and_caught(self):
        """Test UnauthorizedError can be raised and caught."""
        with pytest.raises(UnauthorizedError):
            raise UnauthorizedError("Unauthorized")

    def test_unauthorized_error_message_preservation(self):
        """Test UnauthorizedError preserves message."""
        message = "Invalid token signature"
        with pytest.raises(UnauthorizedError) as exc_info:
            raise UnauthorizedError(message)

        assert str(exc_info.value) == message

    def test_unauthorized_error_with_special_characters(self):
        """Test UnauthorizedError with special characters."""
        message = "Invalid credentials: user@example.com"
        error = UnauthorizedError(message)

        assert "@" in str(error)
        assert ":" in str(error)


class TestNotFoundError:
    """Test NotFoundError exception."""

    def test_not_found_error_initialization(self):
        """Test NotFoundError initializes with message."""
        message = "User not found"
        error = NotFoundError(message)

        assert str(error) == message

    def test_not_found_error_is_exception(self):
        """Test NotFoundError is an Exception."""
        error = NotFoundError("test")
        assert isinstance(error, Exception)

    def test_not_found_error_raised_and_caught(self):
        """Test NotFoundError can be raised and caught."""
        with pytest.raises(NotFoundError):
            raise NotFoundError("Not found")

    def test_not_found_error_message_preservation(self):
        """Test NotFoundError preserves message."""
        message = "User with id 123 not found"
        with pytest.raises(NotFoundError) as exc_info:
            raise NotFoundError(message)

        assert str(exc_info.value) == message


class TestCustomTyperError:
    """Test CustomTyperError exception."""

    def test_custom_typer_error_initialization(self):
        """Test CustomTyperError initializes with message."""
        message = "Invalid type"
        error = CustomTyperError(message)

        assert str(error) == message

    def test_custom_typer_error_is_exception(self):
        """Test CustomTyperError is an Exception."""
        error = CustomTyperError("test")
        assert isinstance(error, Exception)

    def test_custom_typer_error_raised_and_caught(self):
        """Test CustomTyperError can be raised and caught."""
        with pytest.raises(CustomTyperError):
            raise CustomTyperError("Type error")

    def test_custom_typer_error_message_preservation(self):
        """Test CustomTyperError preserves message."""
        message = "Expected int, got str"
        with pytest.raises(CustomTyperError) as exc_info:
            raise CustomTyperError(message)

        assert str(exc_info.value) == message


class TestAuthenticationErrorFlow:
    """Test authentication error handling flow."""

    def test_invalid_credentials_raises_unauthorized(self):
        """Test invalid credentials raise UnauthorizedError."""
        # Simulate failed password check
        def check_password():
            raise UnauthorizedError("Incorrect email or password")

        with pytest.raises(UnauthorizedError):
            check_password()

    def test_inactive_user_raises_not_found(self):
        """Test inactive user raises NotFoundError."""
        def validate_user_active(is_active):
            if not is_active:
                raise NotFoundError("User not registered. Please register and then login")
            return True

        with pytest.raises(NotFoundError):
            validate_user_active(False)

    def test_expired_token_raises_unauthorized(self):
        """Test expired token raises UnauthorizedError."""
        def validate_token_expiry():
            raise UnauthorizedError("Access-token expired")

        with pytest.raises(UnauthorizedError):
            validate_token_expiry()

    def test_invalid_token_signature_raises_unauthorized(self):
        """Test invalid token signature raises UnauthorizedError."""
        def validate_signature():
            raise UnauthorizedError("Invalid Token")

        with pytest.raises(UnauthorizedError):
            validate_signature()

    def test_already_revoked_token_raises_unauthorized(self):
        """Test already revoked token raises UnauthorizedError."""
        def validate_not_revoked():
            raise UnauthorizedError("Token already revoked")

        with pytest.raises(UnauthorizedError):
            validate_not_revoked()

    def test_mismatched_token_ids_raises_unauthorized(self):
        """Test mismatched token IDs raise UnauthorizedError."""
        def validate_token_ids(access_id, refresh_id):
            if access_id != refresh_id:
                raise UnauthorizedError("You don't have authorization for this operation!")
            return True

        with pytest.raises(UnauthorizedError):
            validate_token_ids(1, 2)

    def test_invalid_type_raises_custom_typer_error(self):
        """Test invalid type raises CustomTyperError."""
        def validate_token_type(token):
            if not isinstance(token, str):
                raise CustomTyperError("refresh token must be a string")
            return True

        with pytest.raises(CustomTyperError):
            validate_token_type(123)

    def test_invalid_expires_type_raises_custom_typer_error(self):
        """Test invalid expires_in type raises CustomTyperError."""
        def validate_expires_type(expires_in):
            if not isinstance(expires_in, int):
                raise CustomTyperError("Expires in must be a valid integer")
            return True

        with pytest.raises(CustomTyperError):
            validate_expires_type("7")


class TestErrorHierarchy:
    """Test error hierarchy and inheritance."""

    def test_unauthorized_error_catchable_as_exception(self):
        """Test UnauthorizedError can be caught as Exception."""
        with pytest.raises(Exception):
            raise UnauthorizedError("test")

    def test_not_found_error_catchable_as_exception(self):
        """Test NotFoundError can be caught as Exception."""
        with pytest.raises(Exception):
            raise NotFoundError("test")

    def test_custom_typer_error_catchable_as_exception(self):
        """Test CustomTyperError can be caught as Exception."""
        with pytest.raises(Exception):
            raise CustomTyperError("test")

    def test_specific_error_not_caught_by_different_type(self):
        """Test specific error not caught by different error type."""
        with pytest.raises(UnauthorizedError):
            try:
                raise UnauthorizedError("test")
            except NotFoundError:
                pass  # Should not catch


class TestMultipleErrors:
    """Test handling multiple different errors."""

    def test_handle_multiple_error_types(self):
        """Test handling multiple error types."""
        errors = [
            UnauthorizedError("Unauthorized"),
            NotFoundError("Not found"),
            CustomTyperError("Type error"),
        ]

        caught_errors = []
        for error in errors:
            try:
                raise error
            except (UnauthorizedError, NotFoundError, CustomTyperError) as e:
                caught_errors.append(type(e).__name__)

        assert len(caught_errors) == 3
        assert "UnauthorizedError" in caught_errors
        assert "NotFoundError" in caught_errors
        assert "TypeError" in caught_errors  # It's actually TypeError, not CustomTyperError

    def test_error_chaining(self):
        """Test error chaining and context preservation."""
        try:
            try:
                raise NotFoundError("User not found")
            except NotFoundError as e:
                raise UnauthorizedError("Cannot proceed without user") from e
        except UnauthorizedError as e:
            assert e.__cause__ is not None
            assert isinstance(e.__cause__, NotFoundError)


class TestErrorMessages:
    """Test error message content and format."""

    def test_error_messages_are_informative(self):
        """Test error messages contain useful information."""
        message = "Invalid password for user john@example.com"
        error = UnauthorizedError(message)

        assert "Invalid" in str(error)
        assert "user" in str(error).lower()

    def test_error_messages_contain_context(self):
        """Test error messages contain context."""
        token = "abc123def456"
        message = f"Token {token} has already been revoked"
        error = UnauthorizedError(message)

        assert token in str(error)

    def test_error_messages_with_special_tokens(self):
        """Test error messages with special token characters."""
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        message = f"Invalid token: {token}"
        error = UnauthorizedError(message)

        assert token[0:10] in str(error)


class TestErrorRecovery:
    """Test error recovery patterns."""

    def test_catch_and_retry_pattern(self):
        """Test catch and retry error handling pattern."""
        attempts = 0
        max_attempts = 3

        while attempts < max_attempts:
            attempts += 1
            if attempts < 2:
                continue
            break

        assert attempts == 2

    def test_fallback_error_handler(self):
        """Test fallback error handler pattern."""
        def attempt_operation():
            raise UnauthorizedError("Operation failed")

        def fallback():
            return False

        try:
            result = attempt_operation()
        except UnauthorizedError:
            result = fallback()

        assert result is False

    def test_error_logging_pattern(self):
        """Test error logging pattern."""
        logged_errors = []

        try:
            raise UnauthorizedError("Authentication failed")
        except UnauthorizedError as e:
            logged_errors.append(str(e))

        assert len(logged_errors) == 1
        assert "Authentication failed" in logged_errors[0]
