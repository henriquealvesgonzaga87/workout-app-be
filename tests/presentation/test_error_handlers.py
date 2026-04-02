from unittest.mock import Mock

import pytest
from fastapi import status
from fastapi.responses import JSONResponse

from app.presentation.error_handlers.error import Error
from app.presentation.error_handlers.error_handler import ErrorHandler
from app.presentation.error_handlers.integrity_error import IntegrityError
from app.presentation.error_handlers.reponse_error import ResponseError
from app.presentation.error_handlers.request_error import RequestError


class TestErrorBaseClass:
    """Test suite for Error base class."""

    def test_error_initialization(self):
        """Test Error class initialization."""
        error = Error(message="Test error message")
        assert error.message == "Test error message"

    def test_error_string_representation(self):
        """Test Error string representation."""
        error = Error(message="Test error")
        assert str(error) == "Test error"

    def test_error_is_exception(self):
        """Test that Error is an Exception."""
        error = Error(message="Test")
        assert isinstance(error, Exception)

    def test_error_with_special_characters(self):
        """Test Error with special characters in message."""
        message = "Error: Invalid < > \" ' & characters"
        error = Error(message=message)
        assert error.message == message
        assert str(error) == message


class TestResponseError:
    """Test suite for ResponseError."""

    def test_response_error_initialization(self):
        """Test ResponseError initialization."""
        error = ResponseError(message="Response error occurred")
        assert error.message == "Response error occurred"

    def test_response_error_is_error_subclass(self):
        """Test that ResponseError is a subclass of Error."""
        error = ResponseError(message="Test")
        assert isinstance(error, Error)

    def test_response_error_string_representation(self):
        """Test ResponseError string representation."""
        error = ResponseError(message="Test response error")
        assert str(error) == "Test response error"

    def test_response_error_with_validation_error_message(self):
        """Test ResponseError with validation error message."""
        error = ResponseError(message="Unable to respond the request! Error: validation failed")
        assert "validation failed" in str(error)


class TestRequestError:
    """Test suite for RequestError."""

    def test_request_error_initialization(self):
        """Test RequestError initialization."""
        error = RequestError(message="Bad request")
        assert error.message == "Bad request"

    def test_request_error_is_error_subclass(self):
        """Test that RequestError is a subclass of Error."""
        error = RequestError(message="Test")
        assert isinstance(error, Error)

    def test_request_error_string_representation(self):
        """Test RequestError string representation."""
        error = RequestError(message="Invalid request data")
        assert str(error) == "Invalid request data"

    def test_request_error_with_field_error_message(self):
        """Test RequestError with field validation error."""
        error = RequestError(message="Error while processing the request! Bad Request! Error: field validation")
        assert "field validation" in str(error)


class TestIntegrityError:
    """Test suite for IntegrityError."""

    def test_integrity_error_initialization(self):
        """Test IntegrityError initialization."""
        error = IntegrityError(message="Duplicate entry")
        assert error.message == "Duplicate entry"

    def test_integrity_error_is_error_subclass(self):
        """Test that IntegrityError is a subclass of Error."""
        error = IntegrityError(message="Test")
        assert isinstance(error, Error)

    def test_integrity_error_string_representation(self):
        """Test IntegrityError string representation."""
        error = IntegrityError(message="Duplicate email address")
        assert str(error) == "Duplicate email address"

    def test_integrity_error_with_db_error_message(self):
        """Test IntegrityError with database integrity error message."""
        error = IntegrityError(message="Error to save into DB! Error: UNIQUE constraint failed")
        assert "UNIQUE constraint" in str(error)


class TestErrorHandler:
    """Test suite for ErrorHandler."""

    def test_response_error_handler(self):
        """Test response_error_handler method."""
        request = Mock()
        error = ResponseError(message="Internal server error")

        response = ErrorHandler.response_error_handler(request=request, exc=error)

        assert isinstance(response, JSONResponse)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.body is not None

    def test_response_error_handler_content(self):
        """Test response_error_handler returns correct content."""
        request = Mock()
        error = ResponseError(message="Test error message")

        response = ErrorHandler.response_error_handler(request=request, exc=error)

        # Response content should contain the error message
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_request_error_handler(self):
        """Test request_error_handler method."""
        request = Mock()
        error = RequestError(message="Bad request")

        response = ErrorHandler.request_error_handler(request=request, exc=error)

        assert isinstance(response, JSONResponse)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_request_error_handler_status_code(self):
        """Test request_error_handler returns 400 status."""
        request = Mock()
        error = RequestError(message="Invalid input")

        response = ErrorHandler.request_error_handler(request=request, exc=error)

        assert response.status_code == 400

    def test_integrity_error_handler(self):
        """Test integrity_error_handler method."""
        request = Mock()
        error = IntegrityError(message="Duplicate entry")

        response = ErrorHandler.integrity_error_handler(request=request, exc=error)

        assert isinstance(response, JSONResponse)
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_integrity_error_handler_status_code(self):
        """Test integrity_error_handler returns 409 status."""
        request = Mock()
        error = IntegrityError(message="Email already exists")

        response = ErrorHandler.integrity_error_handler(request=request, exc=error)

        assert response.status_code == 409

    def test_error_handlers_with_different_messages(self):
        """Test error handlers with various messages."""
        request = Mock()
        messages = [
            "Simple error",
            "Error with special chars: @#$%^&*()",
            "Multi-line\nerror message",
            "Unicode error: 你好世界"
        ]

        for msg in messages:
            response_err = ResponseError(message=msg)
            request_err = RequestError(message=msg)
            integrity_err = IntegrityError(message=msg)

            resp1 = ErrorHandler.response_error_handler(request=request, exc=response_err)
            resp2 = ErrorHandler.request_error_handler(request=request, exc=request_err)
            resp3 = ErrorHandler.integrity_error_handler(request=request, exc=integrity_err)

            assert resp1.status_code == 500
            assert resp2.status_code == 400
            assert resp3.status_code == 409

    def test_response_error_handler_500_status(self):
        """Test that response error handler returns 500 status."""
        request = Mock()
        error = ResponseError(message="Unable to respond")

        response = ErrorHandler.response_error_handler(request=request, exc=error)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.status_code == 500

    def test_all_error_types_are_exceptions(self):
        """Test that all error types can be raised as exceptions."""
        errors = [
            ResponseError("test"),
            RequestError("test"),
            IntegrityError("test")
        ]

        for error in errors:
            with pytest.raises(Exception):
                raise error

    def test_error_handler_with_mock_request(self):
        """Test error handlers work with mock request objects."""
        mock_request = Mock()
        mock_request.url = "http://test.com/api"

        error = ResponseError(message="Test error")
        response = ErrorHandler.response_error_handler(request=mock_request, exc=error)

        assert response.status_code == 500
