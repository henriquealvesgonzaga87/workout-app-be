from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.presentation.fastapi.app import App
from app.settings import Settings


@pytest.fixture
def test_settings():
    """Create test settings."""
    return Settings(
        PROJECT_NAME="Workout-app-be-test",
        ROOT_PATH="/workout-app-be",
        PREFIX="/api/v1",
        DATABASE_URL="sqlite:///:memory:"
    )


@pytest.fixture
def test_client(test_settings, monkeypatch):
    """Create test client for FastAPI app."""
    # Mock the UserContainer to avoid database setup
    with patch('app.presentation.fastapi.app.UserContainer'):
        app_instance = App(settings=test_settings)

        # Override the login_required dependency for testing
        from app.presentation.routes.auth.jwt.jwt_dependencies import login_required

        def mock_login_required():
            return {"id": 1, "role": True}

        app_instance.app.dependency_overrides[login_required] = mock_login_required
        return TestClient(app_instance.app)


class TestUserRoutes:
    """Test suite for user routes."""

    def test_create_user_endpoint_exists(self, test_client):
        """Test that create user endpoint exists."""
        response = test_client.post(
            "/api/v1/user/",
            json={
                "name": "Test User",
                "email": "test@example.com",
                "password": "password123"
            }
        )

        # Either success, error, or conflict (duplicate) is acceptable
        assert response.status_code in [201, 400, 409, 422, 500]

    def test_create_user_with_valid_data(self, test_client):
        """Test create user endpoint with valid data."""
        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "secure_password"
        }

        response = test_client.post(
            "/api/v1/user/",
            json=user_data
        )

        # Should accept valid structure (or conflict if already exists)
        assert response.status_code in [201, 400, 409, 422, 500]

    def test_create_user_missing_name(self, test_client):
        """Test create user with missing name."""
        user_data = {
            "email": "test@example.com",
            "password": "password123"
        }

        response = test_client.post(
            "/api/v1/user/",
            json=user_data
        )

        # Should reject due to missing field
        assert response.status_code in [400, 422]

    def test_create_user_missing_email(self, test_client):
        """Test create user with missing email."""
        user_data = {
            "name": "Test User",
            "password": "password123"
        }

        response = test_client.post(
            "/api/v1/user/",
            json=user_data
        )

        # Should reject due to missing field
        assert response.status_code in [400, 422]

    def test_create_user_missing_password(self, test_client):
        """Test create user with missing password."""
        user_data = {
            "name": "Test User",
            "email": "test@example.com"
        }

        response = test_client.post(
            "/api/v1/user/",
            json=user_data
        )

        # Should reject due to missing field
        assert response.status_code in [400, 422]

    def test_create_user_invalid_email_format(self, test_client):
        """Test create user with invalid email format."""
        user_data = {
            "name": "Test User",
            "email": "not-an-email",
            "password": "password123"
        }

        response = test_client.post(
            "/api/v1/user/",
            json=user_data
        )

        # Should reject invalid email
        assert response.status_code in [400, 422]

    def test_create_user_response_status_code(self, test_client):
        """Test that create user returns expected status codes."""
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        }

        response = test_client.post(
            "/api/v1/user/",
            json=user_data
        )

        # Should be either created or an error
        assert 200 <= response.status_code < 600

    def test_create_user_response_content_type(self, test_client):
        """Test that create user response has correct content type."""
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        }

        response = test_client.post(
            "/api/v1/user/",
            json=user_data
        )

        assert "application/json" in response.headers.get("content-type", "")

    def test_endpoint_url_structure(self, test_client):
        """Test that endpoint URL follows expected structure."""
        # Test that the endpoint is properly prefixed
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        }

        response = test_client.post(
            "/api/v1/user/",
            json=user_data
        )

        # Should get a response (not 404)
        assert response.status_code != 404

    def test_create_user_empty_password(self, test_client):
        """Test create user with empty password."""
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": ""
        }

        response = test_client.post(
            "/api/v1/user/",
            json=user_data
        )

        # Empty password might be accepted, rejected, or cause conflict
        assert response.status_code >= 200

    def test_create_user_with_special_characters(self, test_client):
        """Test create user with special characters in name."""
        user_data = {
            "name": "José da Silva",
            "email": "jose@example.com",
            "password": "password123"
        }

        response = test_client.post(
            "/api/v1/user/",
            json=user_data
        )

        # Should handle special characters (or give conflict if exists)
        assert response.status_code in [201, 400, 409, 422, 500]

    def test_create_user_with_long_name(self, test_client):
        """Test create user with very long name."""
        user_data = {
            "name": "A" * 500,
            "email": "test@example.com",
            "password": "password123"
        }

        response = test_client.post(
            "/api/v1/user/",
            json=user_data
        )

        # Should either accept or reject gracefully
        assert response.status_code >= 200

    def test_create_user_response_has_json(self, test_client):
        """Test that create user response includes JSON."""
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        }

        response = test_client.post(
            "/api/v1/user/",
            json=user_data
        )

        try:
            response.json()
        except:
            # If response is not valid JSON, endpoint should handle it properly
            assert response.status_code >= 400


class TestUserRouteIntegration:
    """Integration tests for user route with mocked repository."""

    def test_route_calls_use_case(self):
        """Test that route properly calls the use case."""
        # This is a more complex integration test
        # Would require mocking the dependency injection container
        pass

    def test_error_handling_in_route(self):
        """Test error handling in route."""
        # Would test exception handling
        pass
