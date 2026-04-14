
import pytest

from app.application.user.use_cases.delete_user_use_case import DeleteUserUseCase
from app.presentation.error_handlers.reponse_error import ResponseError
from app.presentation.error_handlers.request_error import RequestError


class TestDeleteUserUseCase:
    """Test suite for DeleteUserUseCase."""

    def test_delete_user_use_case_initialization(self, mock_user_repository):
        """Test that use case initializes correctly."""
        use_case = DeleteUserUseCase(user_repository=mock_user_repository)
        assert use_case.user_repository == mock_user_repository

    def test_prepare_method_with_valid_integer_id(self, mock_user_repository, mock_access_token_payload):
        """Test prepare method with a valid integer ID."""
        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        result = use_case.prepare(id=1, access_token_payload=mock_access_token_payload)

        assert result == 1
        assert isinstance(result, int)

    def test_prepare_method_with_string_integer_id(self, mock_user_repository, mock_access_token_payload):
        """Test prepare method converts string integer to int."""
        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        result = use_case.prepare(id="42", access_token_payload=mock_access_token_payload)

        assert result == 42
        assert isinstance(result, int)

    def test_prepare_method_with_large_id(self, mock_user_repository, mock_access_token_payload):
        """Test prepare method with large ID."""
        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        large_id = 999999
        result = use_case.prepare(id=large_id, access_token_payload=mock_access_token_payload)

        assert result == large_id

    def test_prepare_method_with_invalid_id_raises_error(self, mock_user_repository, mock_access_token_payload):
        """Test prepare method raises RequestError with invalid ID."""
        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        with pytest.raises(RequestError) as exc_info:
            use_case.prepare(id="invalid_id", access_token_payload=mock_access_token_payload)

        assert "Expecting int" in str(exc_info.value)

    def test_prepare_method_with_none_id_raises_error(self, mock_user_repository, mock_access_token_payload):
        """Test prepare method raises RequestError with None ID."""
        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        with pytest.raises(RequestError) as exc_info:
            use_case.prepare(id=None, access_token_payload=mock_access_token_payload)

        assert "Expecting int" in str(exc_info.value)

    def test_prepare_method_with_float_id(self, mock_user_repository, mock_access_token_payload):
        """Test prepare method converts float to int."""
        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        result = use_case.prepare(id=3.14, access_token_payload=mock_access_token_payload)

        # Float gets converted to int (truncated)
        assert result == 3
        assert isinstance(result, int)

    def test_execute_deletes_user_successfully(self, mock_user_repository, mock_access_token_payload):
        """Test successful user deletion."""
        mock_user_repository.delete.return_value = True

        use_case = DeleteUserUseCase(user_repository=mock_user_repository)
        result = use_case.execute(id=1, access_token_payload=mock_access_token_payload)

        assert result is True
        mock_user_repository.delete.assert_called_once_with(id=1)

    def test_execute_returns_boolean(self, mock_user_repository, mock_access_token_payload):
        """Test that execute returns a boolean."""
        mock_user_repository.delete.return_value = True

        use_case = DeleteUserUseCase(user_repository=mock_user_repository)
        result = use_case.execute(id=42, access_token_payload=mock_access_token_payload)

        assert isinstance(result, bool)
        assert result is True

    def test_execute_calls_prepare_before_delete(self, mock_user_repository, mock_access_token_payload):
        """Test that execute prepares the ID before deleting."""
        mock_user_repository.delete.return_value = True

        use_case = DeleteUserUseCase(user_repository=mock_user_repository)
        result = use_case.execute(id="123", access_token_payload=mock_access_token_payload)

        # Should not raise an error and should succeed
        assert result is True
        mock_user_repository.delete.assert_called_once()

    def test_execute_with_string_integer_id(self, mock_user_repository, mock_access_token_payload):
        """Test execute with string integer ID that gets converted."""
        mock_user_repository.delete.return_value = True

        use_case = DeleteUserUseCase(user_repository=mock_user_repository)
        result = use_case.execute(id="99", access_token_payload=mock_access_token_payload)

        assert result is True
        mock_user_repository.delete.assert_called_once()

    def test_execute_with_invalid_id_raises_error(self, mock_user_repository, mock_access_token_payload):
        """Test execute raises RequestError with invalid ID."""
        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        with pytest.raises(RequestError):
            use_case.execute(id="not_an_integer", access_token_payload=mock_access_token_payload)

    def test_execute_propagates_validation_error(self, mock_user_repository, mock_access_token_payload):
        """Test that execute propagates ResponseValidationError as ResponseError."""
        from fastapi.exceptions import ResponseValidationError

        # Create a mock ResponseValidationError
        error = ResponseValidationError("test error")
        mock_user_repository.delete.side_effect = error

        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        with pytest.raises(ResponseError):
            use_case.execute(id=1, access_token_payload=mock_access_token_payload)

    def test_execute_multiple_deletions(self, mock_user_repository, mock_access_token_payload):
        """Test executing multiple delete operations."""
        mock_user_repository.delete.return_value = True

        use_case = DeleteUserUseCase(user_repository=mock_user_repository)

        result1 = use_case.execute(id=1, access_token_payload=mock_access_token_payload)
        result2 = use_case.execute(id=2, access_token_payload=mock_access_token_payload)
        result3 = use_case.execute(id=3, access_token_payload=mock_access_token_payload)

        assert result1 is True
        assert result2 is True
        assert result3 is True
        assert mock_user_repository.delete.call_count == 3

    def test_execute_with_zero_id(self, mock_user_repository, mock_access_token_payload):
        """Test execute with zero ID."""
        mock_user_repository.delete.return_value = True

        use_case = DeleteUserUseCase(user_repository=mock_user_repository)
        result = use_case.execute(id=0, access_token_payload=mock_access_token_payload)

        assert result is True
        mock_user_repository.delete.assert_called_once_with(id=0)

    def test_execute_with_negative_id(self, mock_user_repository, mock_access_token_payload):
        """Test execute with negative ID."""
        mock_user_repository.delete.return_value = True

        use_case = DeleteUserUseCase(user_repository=mock_user_repository)
        result = use_case.execute(id=-1, access_token_payload=mock_access_token_payload)

        assert result is True
        mock_user_repository.delete.assert_called_once_with(id=-1)
