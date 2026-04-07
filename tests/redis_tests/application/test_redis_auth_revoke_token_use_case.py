"""Tests for Redis Auth Revoke Token Use Case."""


import pytest

from app.application.redis.auth.use_cases.redis_auth_revoke_token_use_cases import RedisAuthRevokeTokenUseCase
from app.presentation.error_handlers.type_error import TypeError as CustomTyperError
from app.presentation.error_handlers.unauthorized_error import UnauthorizedError


class TestRedisAuthRevokeTokenUseCaseInitialization:
    """Test Redis Auth Revoke Token Use Case initialization."""

    def test_use_case_initialization(self, mock_redis_auth_repository):
        """Test use case initializes with redis auth repository."""
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        assert use_case.redis_auth_respository == mock_redis_auth_repository

    def test_use_case_stores_repository(self, mock_redis_auth_repository):
        """Test use case stores repository correctly."""
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        assert hasattr(use_case, 'redis_auth_respository')


class TestRedisAuthRevokeTokenUseCasePrepare:
    """Test the prepare method of Redis Auth Revoke Token Use Case."""

    def test_prepare_with_valid_inputs(
        self,
        mock_redis_auth_repository,
        mock_refresh_token,
        mock_expires_in
    ):
        """Test prepare method with valid inputs."""
        mock_redis_auth_repository.is_refresh_token_revoked.return_value = None
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        # Should not raise
        use_case.prepare(
            refresh_token=mock_refresh_token,
            expires_in=mock_expires_in
        )

    def test_prepare_validates_refresh_token_is_string(
        self,
        mock_redis_auth_repository,
        mock_expires_in
    ):
        """Test prepare method validates refresh token is string."""
        mock_redis_auth_repository.is_refresh_token_revoked.return_value = None
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        with pytest.raises(CustomTyperError) as exc_info:
            use_case.prepare(
                refresh_token=123,  # Not a string
                expires_in=mock_expires_in
            )

        assert "refresh token must be a string" in str(exc_info.value)

    def test_prepare_validates_expires_in_is_integer(
        self,
        mock_redis_auth_repository,
        mock_refresh_token
    ):
        """Test prepare method validates expires_in is integer."""
        mock_redis_auth_repository.is_refresh_token_revoked.return_value = None
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        with pytest.raises(CustomTyperError) as exc_info:
            use_case.prepare(
                refresh_token=mock_refresh_token,
                expires_in="7"  # Not an integer
            )

        assert "Expires in must be a valid integer" in str(exc_info.value)

    def test_prepare_validates_expires_in_is_not_float(
        self,
        mock_redis_auth_repository,
        mock_refresh_token
    ):
        """Test prepare method validates expires_in is not float."""
        mock_redis_auth_repository.is_refresh_token_revoked.return_value = None
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        with pytest.raises(CustomTyperError):
            use_case.prepare(
                refresh_token=mock_refresh_token,
                expires_in=7.5  # Float instead of int
            )

    def test_prepare_checks_if_token_already_revoked(
        self,
        mock_redis_auth_repository,
        mock_refresh_token,
        mock_expires_in
    ):
        """Test prepare method checks if token is already revoked."""
        mock_redis_auth_repository.is_refresh_token_revoked.return_value = True
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        with pytest.raises(UnauthorizedError) as exc_info:
            use_case.prepare(
                refresh_token=mock_refresh_token,
                expires_in=mock_expires_in
            )

        assert "Token already revoked" in str(exc_info.value)

    def test_prepare_calls_repository_is_refresh_token_revoked(
        self,
        mock_redis_auth_repository,
        mock_refresh_token,
        mock_expires_in
    ):
        """Test prepare method calls repository is_refresh_token_revoked."""
        mock_redis_auth_repository.is_refresh_token_revoked.return_value = None
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        use_case.prepare(
            refresh_token=mock_refresh_token,
            expires_in=mock_expires_in
        )

        mock_redis_auth_repository.is_refresh_token_revoked.assert_called_once_with(
            refresh_token=mock_refresh_token
        )

    def test_prepare_with_none_token_raises_error(
        self,
        mock_redis_auth_repository,
        mock_expires_in
    ):
        """Test prepare method with None token raises error."""
        mock_redis_auth_repository.is_refresh_token_revoked.return_value = None
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        with pytest.raises(CustomTyperError):
            use_case.prepare(
                refresh_token=None,
                expires_in=mock_expires_in
            )

    def test_prepare_with_negative_expires_in(
        self,
        mock_redis_auth_repository,
        mock_refresh_token
    ):
        """Test prepare method with negative expires_in."""
        mock_redis_auth_repository.is_refresh_token_revoked.return_value = None
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        # Should not raise - negative values are still integers
        # Validation might be at repository level
        use_case.prepare(
            refresh_token=mock_refresh_token,
            expires_in=-1
        )

    def test_prepare_with_zero_expires_in(
        self,
        mock_redis_auth_repository,
        mock_refresh_token
    ):
        """Test prepare method with zero expires_in."""
        mock_redis_auth_repository.is_refresh_token_revoked.return_value = None
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        # Should not raise - zero is still an integer
        use_case.prepare(
            refresh_token=mock_refresh_token,
            expires_in=0
        )


class TestRedisAuthRevokeTokenUseCaseExecute:
    """Test the execute method of Redis Auth Revoke Token Use Case."""

    def test_execute_revokes_token_successfully(
        self,
        mock_redis_auth_repository,
        mock_refresh_token,
        mock_expires_in
    ):
        """Test execute method revokes token successfully."""
        mock_redis_auth_repository.is_refresh_token_revoked.return_value = None
        mock_redis_auth_repository.revoke_refresh_token.return_value = True
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        result = use_case.execute(
            refresh_token=mock_refresh_token,
            expires_in=mock_expires_in
        )

        assert result is True

    def test_execute_returns_boolean(
        self,
        mock_redis_auth_repository,
        mock_refresh_token,
        mock_expires_in
    ):
        """Test execute method returns boolean."""
        mock_redis_auth_repository.is_refresh_token_revoked.return_value = None
        mock_redis_auth_repository.revoke_refresh_token.return_value = True
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        result = use_case.execute(
            refresh_token=mock_refresh_token,
            expires_in=mock_expires_in
        )

        assert isinstance(result, bool)

    def test_execute_calls_prepare(
        self,
        mock_redis_auth_repository,
        mock_refresh_token,
        mock_expires_in
    ):
        """Test execute method calls prepare."""
        mock_redis_auth_repository.is_refresh_token_revoked.return_value = None
        mock_redis_auth_repository.revoke_refresh_token.return_value = True
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        use_case.execute(
            refresh_token=mock_refresh_token,
            expires_in=mock_expires_in
        )

        # Verify prepare was called by checking repository calls
        assert mock_redis_auth_repository.is_refresh_token_revoked.called

    def test_execute_calls_repository_revoke_refresh_token(
        self,
        mock_redis_auth_repository,
        mock_refresh_token,
        mock_expires_in
    ):
        """Test execute method calls repository revoke_refresh_token."""
        mock_redis_auth_repository.is_refresh_token_revoked.return_value = None
        mock_redis_auth_repository.revoke_refresh_token.return_value = True
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        use_case.execute(
            refresh_token=mock_refresh_token,
            expires_in=mock_expires_in
        )

        mock_redis_auth_repository.revoke_refresh_token.assert_called_once_with(
            refresh_token=mock_refresh_token,
            expires_in=mock_expires_in
        )

    def test_execute_with_already_revoked_token(
        self,
        mock_redis_auth_repository,
        mock_refresh_token,
        mock_expires_in
    ):
        """Test execute with already revoked token raises error."""
        mock_redis_auth_repository.is_refresh_token_revoked.return_value = True
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        with pytest.raises(UnauthorizedError):
            use_case.execute(
                refresh_token=mock_refresh_token,
                expires_in=mock_expires_in
            )

    def test_execute_with_invalid_token_type(
        self,
        mock_redis_auth_repository,
        mock_expires_in
    ):
        """Test execute with invalid token type raises error."""
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        with pytest.raises(CustomTyperError):
            use_case.execute(
                refresh_token=123,  # Invalid type
                expires_in=mock_expires_in
            )

    def test_execute_with_invalid_expires_in_type(
        self,
        mock_redis_auth_repository,
        mock_refresh_token
    ):
        """Test execute with invalid expires_in type raises error."""
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        with pytest.raises(CustomTyperError):
            use_case.execute(
                refresh_token=mock_refresh_token,
                expires_in="7"  # Invalid type
            )

    def test_execute_returns_false_when_revocation_fails(
        self,
        mock_redis_auth_repository,
        mock_refresh_token,
        mock_expires_in
    ):
        """Test execute returns False when revocation fails."""
        mock_redis_auth_repository.is_refresh_token_revoked.return_value = None
        mock_redis_auth_repository.revoke_refresh_token.return_value = False
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        result = use_case.execute(
            refresh_token=mock_refresh_token,
            expires_in=mock_expires_in
        )

        assert result is False

    def test_execute_with_different_expires_in_values(
        self,
        mock_redis_auth_repository,
        mock_refresh_token
    ):
        """Test execute with different expires_in values."""
        mock_redis_auth_repository.is_refresh_token_revoked.return_value = None
        mock_redis_auth_repository.revoke_refresh_token.return_value = True
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        expires_values = [1, 7, 30, 365]

        for expires_in in expires_values:
            result = use_case.execute(
                refresh_token=mock_refresh_token,
                expires_in=expires_in
            )

            assert result is True

    def test_execute_with_long_token_string(
        self,
        mock_redis_auth_repository,
        mock_expires_in
    ):
        """Test execute with very long token string."""
        long_token = "x" * 1000
        mock_redis_auth_repository.is_refresh_token_revoked.return_value = None
        mock_redis_auth_repository.revoke_refresh_token.return_value = True
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        result = use_case.execute(
            refresh_token=long_token,
            expires_in=mock_expires_in
        )

        assert result is True


class TestRedisAuthRevokeTokenUseCaseIntegration:
    """Integration tests for Redis Auth Revoke Token Use Case."""

    def test_revoke_token_workflow(
        self,
        mock_redis_auth_repository,
        mock_refresh_token,
        mock_expires_in
    ):
        """Test complete token revocation workflow."""
        mock_redis_auth_repository.is_refresh_token_revoked.return_value = None
        mock_redis_auth_repository.revoke_refresh_token.return_value = True
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        # First revocation should succeed
        result1 = use_case.execute(
            refresh_token=mock_refresh_token,
            expires_in=mock_expires_in
        )
        assert result1 is True

        # Second revocation attempt should fail (token already revoked)
        mock_redis_auth_repository.is_refresh_token_revoked.return_value = True

        with pytest.raises(UnauthorizedError):
            use_case.execute(
                refresh_token=mock_refresh_token,
                expires_in=mock_expires_in
            )

    def test_revoke_multiple_different_tokens(
        self,
        mock_redis_auth_repository,
        mock_expires_in
    ):
        """Test revoking multiple different tokens."""
        mock_redis_auth_repository.is_refresh_token_revoked.return_value = None
        mock_redis_auth_repository.revoke_refresh_token.return_value = True
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        tokens = [
            "token_user_1",
            "token_user_2",
            "token_user_3",
        ]

        for token in tokens:
            result = use_case.execute(
                refresh_token=token,
                expires_in=mock_expires_in
            )
            assert result is True

    def test_revoke_token_with_different_expiry_times(
        self,
        mock_redis_auth_repository,
        mock_refresh_token
    ):
        """Test revoking token with different expiry times."""
        mock_redis_auth_repository.is_refresh_token_revoked.return_value = None
        mock_redis_auth_repository.revoke_refresh_token.return_value = True
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        # First revocation
        result1 = use_case.execute(
            refresh_token=mock_refresh_token,
            expires_in=7
        )
        assert result1 is True

    def test_prepare_and_execute_separately(
        self,
        mock_redis_auth_repository,
        mock_refresh_token,
        mock_expires_in
    ):
        """Test calling prepare and execute separately."""
        mock_redis_auth_repository.is_refresh_token_revoked.return_value = None
        mock_redis_auth_repository.revoke_refresh_token.return_value = True
        use_case = RedisAuthRevokeTokenUseCase(
            redis_auth_respository=mock_redis_auth_repository
        )

        # Call prepare
        use_case.prepare(
            refresh_token=mock_refresh_token,
            expires_in=mock_expires_in
        )

        # Then call execute
        result = use_case.execute(
            refresh_token=mock_refresh_token,
            expires_in=mock_expires_in
        )

        assert result is True
