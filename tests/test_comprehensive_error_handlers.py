"""
Comprehensive tests for all error handlers.
Covers all error types and edge cases.
"""
import pytest

from app.presentation.error_handlers.atribute_error import AttributeError as CustomAttributeError
from app.presentation.error_handlers.data_base_error import DataBaseError
from app.presentation.error_handlers.error import Error
from app.presentation.error_handlers.integrity_error import IntegrityError
from app.presentation.error_handlers.not_found_error import NotFoundError
from app.presentation.error_handlers.reponse_error import ResponseError
from app.presentation.error_handlers.request_error import RequestError


class TestAttributeErrorHandler:
    """Test suite for AttributeError custom handler."""

    def test_attribute_error_initialization(self):
        """Test AttributeError initialization."""
        error = CustomAttributeError(message="Cannot set attribute")
        assert error.message == "Cannot set attribute"

    def test_attribute_error_is_error_subclass(self):
        """Test that AttributeError is a subclass of Error."""
        error = CustomAttributeError(message="Test")
        assert isinstance(error, Error)

    def test_attribute_error_string_representation(self):
        """Test AttributeError string representation."""
        error = CustomAttributeError(message="Invalid attribute")
        assert str(error) == "Invalid attribute"

    def test_attribute_error_with_database_context(self):
        """Test AttributeError with database context message."""
        error = CustomAttributeError(message="Impossible to proccess due to db issues: Invalid field access")
        assert "db issues" in str(error)

    def test_attribute_error_with_special_characters(self):
        """Test AttributeError with special characters."""
        message = "Attribute Error: field < > \" ' &"
        error = CustomAttributeError(message=message)
        assert error.message == message

    def test_attribute_error_with_empty_message(self):
        """Test AttributeError with empty message."""
        error = CustomAttributeError(message="")
        assert error.message == ""
        assert str(error) == ""


class TestDataBaseError:
    """Test suite for DataBaseError."""

    def test_database_error_initialization(self):
        """Test DataBaseError initialization."""
        error = DataBaseError(message="Connection failed")
        assert error.message == "Connection failed"

    def test_database_error_is_error_subclass(self):
        """Test that DataBaseError is a subclass of Error."""
        error = DataBaseError(message="Test")
        assert isinstance(error, Error)

    def test_database_error_string_representation(self):
        """Test DataBaseError string representation."""
        error = DataBaseError(message="Database unavailable")
        assert str(error) == "Database unavailable"

    def test_database_error_with_sqlalchemy_error_message(self):
        """Test DataBaseError with SQLAlchemy error details."""
        error = DataBaseError(message="Impossible to proccess right now! Error: [SQLAlchemy Error Details]")
        assert "SQLAlchemy" in str(error)

    def test_database_error_inheritance_chain(self):
        """Test that DataBaseError maintains inheritance chain."""
        error = DataBaseError(message="Test")
        assert isinstance(error, Error)
        assert isinstance(error, Exception)


class TestNotFoundError:
    """Test suite for NotFoundError."""

    def test_not_found_error_initialization(self):
        """Test NotFoundError initialization."""
        error = NotFoundError(message="User not found")
        assert error.message == "User not found"

    def test_not_found_error_is_error_subclass(self):
        """Test that NotFoundError is a subclass of Error."""
        error = NotFoundError(message="Test")
        assert isinstance(error, Error)

    def test_not_found_error_string_representation(self):
        """Test NotFoundError string representation."""
        error = NotFoundError(message="Resource not found")
        assert str(error) == "Resource not found"

    def test_not_found_error_with_user_id(self):
        """Test NotFoundError with user ID details."""
        error = NotFoundError(message="User with ID 123 not found")
        assert "123" in str(error)
        assert "not found" in str(error)

    def test_not_found_error_with_multiple_contexts(self):
        """Test NotFoundError in different contexts."""
        errors = [
            NotFoundError(message="User not found"),
            NotFoundError(message="Resource not found"),
            NotFoundError(message="No result found"),
        ]

        for error in errors:
            assert isinstance(error, Error)
            assert "not found" in str(error).lower() or "no result" in str(error).lower()


class TestIntegrityErrorHandler:
    """Extended test suite for IntegrityError."""

    def test_integrity_error_with_duplicate_email(self):
        """Test IntegrityError with duplicate email context."""
        error = IntegrityError(message="Error to save into DB! Error: Duplicate email")
        assert "Duplicate" in str(error)

    def test_integrity_error_inheritance(self):
        """Test IntegrityError inheritance chain."""
        error = IntegrityError(message="Test")
        assert isinstance(error, Error)
        assert isinstance(error, Exception)

    def test_integrity_error_with_constraint_message(self):
        """Test IntegrityError with database constraint message."""
        error = IntegrityError(message="Error to save into DB! Error: UNIQUE constraint failed")
        assert "constraint" in str(error).lower()


class TestRequestErrorExtended:
    """Extended tests for RequestError."""

    def test_request_error_with_validation_context(self):
        """Test RequestError with validation error context."""
        error = RequestError(message="Unable to proccess the request ValidationError: invalid field")
        assert "proccess" in str(error)

    def test_request_error_exception_handling(self):
        """Test RequestError can be raised and caught."""
        with pytest.raises(RequestError) as exc_info:
            raise RequestError(message="Test request error")

        assert exc_info.value.message == "Test request error"


class TestResponseErrorExtended:
    """Extended tests for ResponseError."""

    def test_response_error_exception_handling(self):
        """Test ResponseError can be raised and caught."""
        with pytest.raises(ResponseError) as exc_info:
            raise ResponseError(message="Test response error")

        assert exc_info.value.message == "Test response error"


class TestErrorHierarchy:
    """Test the error class hierarchy and relationships."""

    def test_all_errors_are_exceptions(self):
        """Test that all custom errors are Exception subclasses."""
        errors = [
            Error(message="test"),
            RequestError(message="test"),
            ResponseError(message="test"),
            IntegrityError(message="test"),
            DataBaseError(message="test"),
            NotFoundError(message="test"),
            CustomAttributeError(message="test"),
        ]

        for error in errors:
            assert isinstance(error, Exception)

    def test_all_errors_preserve_message(self):
        """Test that all errors preserve their messages."""
        test_message = "This is a test error message"
        errors = [
            Error(message=test_message),
            RequestError(message=test_message),
            ResponseError(message=test_message),
            IntegrityError(message=test_message),
            DataBaseError(message=test_message),
            NotFoundError(message=test_message),
            CustomAttributeError(message=test_message),
        ]

        for error in errors:
            assert error.message == test_message
            assert str(error) == test_message

    def test_error_message_accuracy(self):
        """Test that error messages are accurately maintained."""
        message = "Precise error details: code 123, context XYZ"
        error = Error(message=message)
        assert error.message == message
        assert str(error) == message

    def test_custom_error_in_exception_context(self):
        """Test custom errors in try-except context."""
        try:
            raise DataBaseError(message="Database connection lost")
        except DataBaseError as e:
            assert e.message == "Database connection lost"
        except Exception:
            pytest.fail("DataBaseError should be caught by its specific handler")

    def test_custom_error_in_general_exception_context(self):
        """Test custom errors caught as general Exception."""
        try:
            raise NotFoundError(message="Item not found")
        except Exception as e:
            assert isinstance(e, NotFoundError)
            assert e.message == "Item not found"


class TestErrorMessageFormats:
    """Test various error message formats."""

    def test_error_with_long_message(self):
        """Test error with very long message."""
        long_message = "A" * 1000
        error = Error(message=long_message)
        assert error.message == long_message
        assert len(str(error)) == 1000

    def test_error_with_multiline_message(self):
        """Test error with multiline message."""
        message = "Line 1\nLine 2\nLine 3"
        error = Error(message=message)
        assert error.message == message
        assert "\n" in str(error)

    def test_error_with_unicode_message(self):
        """Test error with unicode characters."""
        message = "Erreur: José María 中文 العربية 🚀"
        error = Error(message=message)
        assert error.message == message

    def test_error_with_sql_details(self):
        """Test error with SQL details."""
        message = "DataBaseError: Failed to execute SQL: SELECT * FROM users WHERE id=1"
        error = DataBaseError(message=message)
        assert "SELECT" in str(error)


class TestErrorContext:
    """Test error behavior in different contexts."""

    def test_error_in_list_comprehension(self):
        """Test creating errors in list comprehension."""
        errors = [NotFoundError(message=f"Item {i} not found") for i in range(5)]
        assert len(errors) == 5
        assert all(isinstance(e, NotFoundError) for e in errors)

    def test_raising_and_catching_custom_errors(self):
        """Test raising and catching custom errors."""
        error_types = [
            RequestError,
            IntegrityError,
            DataBaseError,
            NotFoundError,
        ]

        for error_type in error_types:
            with pytest.raises(error_type):
                raise error_type(message="Test")

    def test_error_reraise(self):
        """Test re-raising errors."""
        try:
            raise DataBaseError(message="Original error")
        except DataBaseError:
            with pytest.raises(DataBaseError) as exc_info:
                raise
            assert exc_info.value.message == "Original error"
