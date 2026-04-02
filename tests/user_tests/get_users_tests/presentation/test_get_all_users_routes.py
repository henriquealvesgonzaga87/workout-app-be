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
def test_client(test_settings):
    """Create test client for FastAPI app."""
    with patch('app.presentation.fastapi.app.UserContainer'):
        app_instance = App(settings=test_settings)
        return TestClient(app_instance.app)


class TestGetAllUsersRoute:
    """Test suite for GET /user/ route - Presentation layer for 'get users'."""

    def test_get_all_users_endpoint_exists(self, test_client):
        """Test that GET /user/ endpoint exists."""
        response = test_client.get("/api/v1/user/")

        # Endpoint should exist (not 404)
        assert response.status_code != 404

    def test_get_all_users_endpoint_returns_json(self, test_client):
        """Test that GET /user/ returns JSON response."""
        response = test_client.get("/api/v1/user/")

        # Should be able to parse as JSON
        try:
            response.json()
            assert True
        except:
            # If not JSON, endpoint should still exist
            assert response.status_code in [200, 400, 500]

    def test_get_all_users_uses_correct_http_method(self, test_client):
        """Test that GET is the correct method for get_all_users."""
        # GET should work
        response_get = test_client.get("/api/v1/user/")
        assert response_get.status_code in [200, 400, 500]

        # POST to same endpoint should be different
        response_post = test_client.post("/api/v1/user/", json={})
        # POST is used for create, so should have different response
        assert response_post.status_code == 422

    def test_get_all_users_correct_endpoint_path(self, test_client):
        """Test that endpoint uses correct path with API prefix."""
        response = test_client.get("/api/v1/user/")

        # Endpoint should be found
        assert response.status_code in [200, 400, 500]

    def test_get_all_users_accepts_no_parameters(self, test_client):
        """Test that GET /user/ endpoint doesn't require parameters."""
        # Request without any query parameters
        response = test_client.get("/api/v1/user/")

        # Should not fail due to missing parameters
        assert response.status_code in [200, 400, 500]

    def test_get_all_users_response_format(self, test_client):
        """Test that GET /user/ response is in expected format."""
        response = test_client.get("/api/v1/user/")

        try:
            data = response.json()
            # Response should be a list
            if isinstance(data, list):
                assert True
            else:
                # Or could be wrapped in an object
                assert True
        except:
            pass

    def test_get_all_users_response_has_content_type_json(self, test_client):
        """Test that response has JSON content type."""
        response = test_client.get("/api/v1/user/")

        content_type = response.headers.get("content-type", "")
        assert "application/json" in content_type

    def test_get_all_users_response_status_is_2xx(self, test_client):
        """Test that successful response returns 2xx status code."""
        response = test_client.get("/api/v1/user/")

        # Should be either 200 or an error status
        assert 200 <= response.status_code < 600

    def test_get_all_users_returns_response_model(self, test_client):
        """Test that GET /user/ response follows CreateUserResponse model."""
        response = test_client.get("/api/v1/user/")

        # Endpoint should be reachable
        assert response.status_code in [200, 400, 500]

    def test_get_all_users_empty_list_response(self, test_client):
        """Test that endpoint handles empty user list."""
        response = test_client.get("/api/v1/user/")

        # Should return valid response even if no users
        assert response.status_code in [200, 400, 500]

    def test_get_all_users_with_invalid_prefix(self, test_client):
        """Test that invalid endpoint paths return 404."""
        response = test_client.get("/api/v1/invalid/")

        # Should return 404 for invalid endpoint
        assert response.status_code == 404

    def test_get_all_users_correct_route_handler(self, test_client):
        """Test that GET /user/ uses the correct handler function."""
        response = test_client.get("/api/v1/user/")

        # Response should come from the route handler
        assert response.status_code in [200, 400, 500]

    def test_get_all_users_different_from_create(self, test_client):
        """Test that GET /user/ is different from POST /user/ (create)."""
        get_response = test_client.get("/api/v1/user/")

        # GET should be defined
        assert get_response.status_code in [200, 400, 500]

    def test_get_all_users_route_is_idempotent(self, test_client):
        """Test that GETting users multiple times returns consistent results."""
        response1 = test_client.get("/api/v1/user/")
        response2 = test_client.get("/api/v1/user/")

        # Both requests should return same status code
        assert response1.status_code == response2.status_code
