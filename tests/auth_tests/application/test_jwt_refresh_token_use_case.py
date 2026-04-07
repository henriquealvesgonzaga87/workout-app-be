"""Tests for JWT Refresh Token Use Case."""

from unittest.mock import Mock

import pytest
from jose import jwt

from app.application.auth.jwt.use_cases.jwt_referesh_token_use_case import JwtRefreshTokenUseCases
from app.presentation.error_handlers.type_error import TypeError as CustomTyperError


class TestJwtRefreshTokenUseCaseInitialization:
    """Test JWT Refresh Token Use Case initialization."""

    def test_initialization_with_valid_dependencies(self):
        """Test use case initializes with valid dependencies."""
        mock_jwt_handler = Mock()
        use_case = JwtRefreshTokenUseCases(jwt_handler=mock_jwt_handler)

        assert use_case.jwt_handler == mock_jwt_handler

    def test_initialization_stores_jwt_handler(self):
        """Test use case stores jwt handler correctly."""
        mock_jwt_handler = Mock()
        use_case = JwtRefreshTokenUseCases(jwt_handler=mock_jwt_handler)

        assert hasattr(use_case, 'jwt_handler')


class TestJwtRefreshTokenUseCasePrepare:
    """Test the prepare method of JWT Refresh Token Use Case."""

    def test_prepare_with_valid_token(self):
        """Test prepare method with valid token string."""
        mock_jwt_handler = Mock()
        use_case = JwtRefreshTokenUseCases(jwt_handler=mock_jwt_handler)
        token = "valid_token_string"

        result = use_case.prepare(refresh_token=token)

        assert result == token

    def test_prepare_validates_token_is_string(self):
        """Test prepare method validates token is string."""
        mock_jwt_handler = Mock()
        use_case = JwtRefreshTokenUseCases(jwt_handler=mock_jwt_handler)

        with pytest.raises(CustomTyperError):
            use_case.prepare(refresh_token=123)

    def test_prepare_with_none_token_raises_error(self):
        """Test prepare method with None token raises error."""
        mock_jwt_handler = Mock()
        use_case = JwtRefreshTokenUseCases(jwt_handler=mock_jwt_handler)

        with pytest.raises(CustomTyperError):
            use_case.prepare(refresh_token=None)

    def test_prepare_with_empty_string(self):
        """Test prepare method with empty string token."""
        mock_jwt_handler = Mock()
        use_case = JwtRefreshTokenUseCases(jwt_handler=mock_jwt_handler)

        # Empty string is still a string type
        result = use_case.prepare(refresh_token="")
        assert result == ""

    def test_prepare_returns_same_token(self):
        """Test prepare method returns the same token."""
        mock_jwt_handler = Mock()
        use_case = JwtRefreshTokenUseCases(jwt_handler=mock_jwt_handler)
        token = "some.jwt.token"

        result = use_case.prepare(refresh_token=token)

        assert result is token


class TestJwtRefreshTokenUseCaseExecute:
    """Test the execute method of JWT Refresh Token Use Case."""

    def test_execute_returns_valid_response(
        self,
        jwt_handler,
        valid_refresh_token
    ):
        """Test execute method returns valid response."""
        use_case = JwtRefreshTokenUseCases(jwt_handler=jwt_handler)

        result = use_case.execute(refresh_token=valid_refresh_token)

        # Should have access_token and refresh_token
        assert hasattr(result, 'access_token')
        assert hasattr(result, 'refresh_token')

    def test_execute_returns_not_none_tokens(
        self,
        jwt_handler,
        valid_refresh_token
    ):
        """Test execute method returns non-None tokens."""
        use_case = JwtRefreshTokenUseCases(jwt_handler=jwt_handler)

        result = use_case.execute(refresh_token=valid_refresh_token)

        assert result.access_token is not None
        assert result.refresh_token is not None

    def test_execute_calls_jwt_handler(
        self,
        valid_refresh_token
    ):
        """Test execute method calls jwt_handler.refresh_token."""
        mock_jwt_handler = Mock()
        mock_jwt_handler.refresh_token.return_value = Mock(
            access_token="new_access",
            refresh_token="new_refresh"
        )
        use_case = JwtRefreshTokenUseCases(jwt_handler=mock_jwt_handler)

        use_case.execute(refresh_token=valid_refresh_token)

        mock_jwt_handler.refresh_token.assert_called_once_with(
            refresh_token=valid_refresh_token
        )

    def test_execute_propagates_prepare_errors(
        self,
        jwt_handler
    ):
        """Test execute propagates prepare errors."""
        use_case = JwtRefreshTokenUseCases(jwt_handler=jwt_handler)

        with pytest.raises(CustomTyperError):
            use_case.execute(refresh_token=123)

    def test_execute_preserves_user_id(
        self,
        jwt_handler,
        valid_refresh_token,
        mock_user_entity
    ):
        """Test execute preserves user id in new access token."""
        use_case = JwtRefreshTokenUseCases(jwt_handler=jwt_handler)

        result = use_case.execute(refresh_token=valid_refresh_token)

        # Decode and verify user id is preserved
        decoded = jwt.decode(
            result.access_token,
            jwt_handler.SECRET_KEY,
            algorithms=jwt_handler.ALGORITHM
        )
        assert decoded["id"] == mock_user_entity.id


class TestJwtRefreshTokenUseCaseIntegration:
    """Integration tests for JWT Refresh Token Use Case."""

    def test_refresh_token_workflow(
        self,
        jwt_handler,
        valid_refresh_token
    ):
        """Test complete token refresh workflow."""
        use_case = JwtRefreshTokenUseCases(jwt_handler=jwt_handler)

        # First refresh
        result1 = use_case.execute(refresh_token=valid_refresh_token)
        assert result1.access_token is not None

        # Second refresh with new token
        result2 = use_case.execute(refresh_token=result1.refresh_token)
        assert result2.access_token is not None

    def test_multiple_consecutive_refreshes(
        self,
        jwt_handler,
        valid_refresh_token
    ):
        """Test multiple consecutive token refreshes."""
        use_case = JwtRefreshTokenUseCases(jwt_handler=jwt_handler)

        current_token = valid_refresh_token
        for _i in range(3):
            result = use_case.execute(refresh_token=current_token)
            assert result.access_token is not None
            current_token = result.refresh_token


class TestJwtRefreshTokenUseCaseErrors:
    """Test error handling in JWT Refresh Token Use Case."""

    def test_execute_with_invalid_token_type_int(
        self,
        jwt_handler
    ):
        """Test execute with invalid token type raises error."""
        use_case = JwtRefreshTokenUseCases(jwt_handler=jwt_handler)

        with pytest.raises(CustomTyperError):
            use_case.execute(refresh_token=12345)

    def test_execute_with_list_token(
        self,
        jwt_handler
    ):
        """Test execute with list token raises error."""
        use_case = JwtRefreshTokenUseCases(jwt_handler=jwt_handler)

        with pytest.raises(CustomTyperError):
            use_case.execute(refresh_token=["token"])

    def test_execute_with_dict_token(
        self,
        jwt_handler
    ):
        """Test execute with dict token raises error."""
        use_case = JwtRefreshTokenUseCases(jwt_handler=jwt_handler)

        with pytest.raises(CustomTyperError):
            use_case.execute(refresh_token={"token": "value"})


class TestJwtRefreshTokenUseCaseMembers:
    """Test use case members and attributes."""

    def test_use_case_has_jwt_handler(self):
        """Test use case has jwt_handler attribute."""
        mock_jwt_handler = Mock()
        use_case = JwtRefreshTokenUseCases(jwt_handler=mock_jwt_handler)

        assert hasattr(use_case, 'jwt_handler')
        assert use_case.jwt_handler == mock_jwt_handler

    def test_prepare_is_callable(self):
        """Test prepare method is callable."""
        mock_jwt_handler = Mock()
        use_case = JwtRefreshTokenUseCases(jwt_handler=mock_jwt_handler)

        assert callable(use_case.prepare)

    def test_execute_is_callable(self):
        """Test execute method is callable."""
        mock_jwt_handler = Mock()
        use_case = JwtRefreshTokenUseCases(jwt_handler=mock_jwt_handler)

        assert callable(use_case.execute)
