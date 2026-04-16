
import pytest
from fastapi.exceptions import ResponseValidationError

from app.application.user.use_cases.delete_user_use_case import DeleteUserUseCase
from app.presentation.error_handlers.data_base_error import DataBaseError
from app.presentation.error_handlers.not_found_error import NotFoundError
from app.presentation.error_handlers.reponse_error import ResponseError
from app.presentation.error_handlers.request_error import RequestError


class TestDeleteUserErrorHandling:
    """Test suite for error handling in delete user operations."""

    def test_delete_use_case_handles_request_error(self, mock_user_repository, mock_access_token_payload):
        """Test that DeleteUserUseCase propagates RequestError for invalid ID."""
        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        with pytest.raises(RequestError) as exc_info:
            use_case.execute(id="invalid", access_token_payload=mock_access_token_payload)

        assert "Expecting int" in str(exc_info.value)
        assert isinstance(exc_info.value, RequestError)

    def test_delete_use_case_handles_response_validation_error(self, mock_user_repository, mock_access_token_payload):
        """Test that DeleteUserUseCase converts ResponseValidationError to ResponseError."""
        error = ResponseValidationError("test error")
        mock_user_repository.delete.side_effect = error

        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        with pytest.raises(ResponseError) as exc_info:
            use_case.execute(id=1, access_token_payload=mock_access_token_payload)

        assert "Unable to respond" in str(exc_info.value)
        assert isinstance(exc_info.value, ResponseError)

    def test_delete_use_case_handles_not_found_error_from_repository(
            self, 
            mock_user_repository, 
            mock_access_token_payload
        ):
        """Test that DeleteUserUseCase allows NotFoundError from repository to propagate."""
        mock_user_repository.delete.side_effect = NotFoundError("User not found")

        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        with pytest.raises(NotFoundError) as exc_info:
            use_case.execute(id=1, access_token_payload=mock_access_token_payload)

        assert "not found" in str(exc_info.value).lower()

    def test_delete_use_case_handles_database_error_from_repository(
            self, 
            mock_user_repository, 
            mock_access_token_payload
        ):
        """Test that DeleteUserUseCase allows DataBaseError from repository to propagate."""
        mock_user_repository.delete.side_effect = DataBaseError("Database connection failed")

        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        with pytest.raises(DataBaseError):
            use_case.execute(id=1, access_token_payload=mock_access_token_payload)

    def test_prepare_method_error_message_format(self, mock_user_repository, mock_access_token_payload):
        """Test that prepare method error messages are properly formatted."""
        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        with pytest.raises(RequestError) as exc_info:
            use_case.prepare(id=[1, 2, 3], access_token_payload=mock_access_token_payload)  # List is invalid

        error_msg = str(exc_info.value)
        assert "Expecting int" in error_msg
        assert "list" in error_msg.lower()

    def test_delete_with_none_returns_error(self, mock_user_repository, mock_access_token_payload):
        """Test that passing None as ID returns appropriate error."""
        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        with pytest.raises(RequestError) as exc_info:
            use_case.prepare(id=None, access_token_payload=mock_access_token_payload)

        assert "Expecting int" in str(exc_info.value)

    def test_delete_with_empty_string_raises_error(self, mock_user_repository, mock_access_token_payload):
        """Test that passing empty string as ID raises RequestError."""
        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        with pytest.raises(RequestError):
            use_case.prepare(id="", access_token_payload=mock_access_token_payload)

    def test_delete_with_dict_raises_error(self, mock_user_repository, mock_access_token_payload):
        """Test that passing dict as ID raises RequestError."""
        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        with pytest.raises(RequestError) as exc_info:
            use_case.prepare(id={"id": 1}, access_token_payload=mock_access_token_payload)

        assert "Expecting int" in str(exc_info.value)

    def test_delete_with_object_raises_error(self, mock_user_repository, mock_access_token_payload):
        """Test that passing object as ID raises RequestError."""
        class CustomObject:
            pass

        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        with pytest.raises(RequestError):
            use_case.prepare(id=CustomObject(), access_token_payload=mock_access_token_payload)

    def test_error_message_contains_type_information(self, mock_user_repository, mock_access_token_payload):
        """Test that error message includes the type that was passed."""
        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        with pytest.raises(RequestError) as exc_info:
            use_case.prepare(id={"test": "dict"}, access_token_payload=mock_access_token_payload)

        error_msg = str(exc_info.value)
        assert "dict" in error_msg

    def test_request_error_vs_response_error_distinction(self, mock_user_repository, mock_access_token_payload):
        """Test that RequestError and ResponseError are properly distinguished."""
        error = ResponseValidationError("test error")
        mock_user_repository.delete.side_effect = error

        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        # RequestError for invalid input
        with pytest.raises(RequestError):
            use_case.prepare(id="invalid", access_token_payload=mock_access_token_payload)

        # ResponseError for validation errors from operations
        with pytest.raises(ResponseError):
            use_case.execute(id=1, access_token_payload=mock_access_token_payload)

    def test_multiple_error_types_in_sequence(self, mock_user_repository, mock_access_token_payload):
        """Test handling different error types in sequence."""
        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        # First error: RequestError
        with pytest.raises(RequestError):
            use_case.execute(id="not_int", access_token_payload=mock_access_token_payload)

        # Setup second error: ResponseError
        error = ResponseValidationError("test error")
        mock_user_repository.delete.side_effect = error

        # Second error: ResponseError
        with pytest.raises(ResponseError):
            use_case.execute(id=1, access_token_payload=mock_access_token_payload)

    def test_error_recovery_after_failed_delete(self, mock_user_repository, mock_access_token_payload):
        """Test that use case can recover and execute successfully after an error."""
        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        # First call fails
        mock_user_repository.delete.side_effect = NotFoundError("User not found")
        with pytest.raises(NotFoundError):
            use_case.execute(id=1, access_token_payload=mock_access_token_payload)

        # Setup successful call
        mock_user_repository.delete.side_effect = None
        mock_user_repository.delete.return_value = True

        # Second call succeeds
        result = use_case.execute(id=2, access_token_payload=mock_access_token_payload)
        assert result is True

    def test_database_error_during_preparation(self, mock_user_repository, mock_access_token_payload):
        """Test handling errors during ID preparation."""
        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        # These should raise RequestError, not reach the repository
        error_inputs = [
            "abc",
            [1],
            {"id": 1},
            None,
        ]

        for error_input in error_inputs:
            with pytest.raises(RequestError):
                use_case.prepare(id=error_input, access_token_payload=mock_access_token_payload)

        # Float can be converted, so it won't raise an error
        result = use_case.prepare(id=3.14, access_token_payload=mock_access_token_payload)
        assert result == 3

    def test_error_isolation_between_delete_calls(self, mock_user_repository, mock_access_token_payload):
        """Test that errors don't affect subsequent delete calls."""
        mock_user_repository.delete.return_value = True
        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        # First successful call
        result1 = use_case.execute(id=1, access_token_payload=mock_access_token_payload)
        assert result1 is True

        # Error in between
        with pytest.raises(RequestError):
            use_case.prepare(id="invalid", access_token_payload=mock_access_token_payload)

        # Second successful call should still work
        result2 = use_case.execute(id=2, access_token_payload=mock_access_token_payload)
        assert result2 is True

    def test_prepare_error_with_boundary_values(self, mock_user_repository, mock_access_token_payload):
        """Test prepare method with boundary and edge case values."""
        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        # Valid boundary values
        assert use_case.prepare(id=0, access_token_payload=mock_access_token_payload) == 0
        assert use_case.prepare(id=1, access_token_payload=mock_access_token_payload) == 1
        assert use_case.prepare(id="0", access_token_payload=mock_access_token_payload) == 0
        assert use_case.prepare(id="999999999", access_token_payload=mock_access_token_payload) == 999999999

    def test_custom_error_message_in_request_error(self, mock_user_repository, mock_access_token_payload):
        """Test that RequestError includes helpful error messages."""
        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        with pytest.raises(RequestError) as exc_info:
            use_case.prepare(id={"invalid": "dict"}, access_token_payload=mock_access_token_payload)

        error_message = str(exc_info.value)
        assert "Expecting int" in error_message
        assert "dict" in error_message.lower()
