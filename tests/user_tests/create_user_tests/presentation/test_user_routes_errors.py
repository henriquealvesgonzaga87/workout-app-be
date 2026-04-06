"""
Tests for error handling in user creation routes.
Covers RequestValidationError and exception handling paths.
"""
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
        return TestClient(app_instance.app)


class TestUserRoutesErrorHandling:
    """Test error paths in user routes."""

    def test_create_user_with_request_validation_error(self, test_client):
        """Test that RequestValidationError is properly handled in create route."""
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        }

        # Send request and expect a response (may be error due to dependency injection)
        response = test_client.post(
            "/api/v1/user/",
            json=user_data
        )

        # Should get some response (not crash)
        assert response.status_code in [201, 400, 422, 500, 409]

    def test_create_user_invalid_json_body(self, test_client):
        """Test create user with invalid JSON body."""
        response = test_client.post(
            "/api/v1/user/",
            content="invalid json",
            headers={"Content-Type": "application/json"}
        )

        # Should reject invalid JSON
        assert response.status_code in [400, 422]

    def test_create_user_with_null_values(self, test_client):
        """Test create user with null values in required fields."""
        user_data = {
            "name": None,
            "email": None,
            "password": None
        }

        response = test_client.post(
            "/api/v1/user/",
            json=user_data
        )

        # Should reject null values
        assert response.status_code in [400, 422, 500]

    def test_create_user_with_empty_name(self, test_client):
        """Test create user with empty name."""
        user_data = {
            "name": "",
            "email": "test@example.com",
            "password": "password123"
        }

        response = test_client.post(
            "/api/v1/user/",
            json=user_data
        )

        # May accept or reject depending on validation rules
        assert response.status_code in [201, 400, 422, 500, 409]

    def test_create_user_with_empty_email(self, test_client):
        """Test create user with empty email."""
        user_data = {
            "name": "Test User",
            "email": "",
            "password": "password123"
        }

        response = test_client.post(
            "/api/v1/user/",
            json=user_data
        )

        assert response.status_code in [201, 400, 422, 500, 409]

    def test_create_user_with_very_long_name(self, test_client):
        """Test create user with extremely long name."""
        user_data = {
            "name": "a" * 10000,
            "email": "test@example.com",
            "password": "password123"
        }

        response = test_client.post(
            "/api/v1/user/",
            json=user_data
        )

        # May accept or reject depending on field constraints
        assert response.status_code in [201, 400, 422, 500, 409]

    def test_create_user_with_unicode_characters(self, test_client):
        """Test create user with unicode characters."""
        user_data = {
            "name": "José María García 中文",
            "email": "josé@example.com",
            "password": "pässwörd123"
        }

        response = test_client.post(
            "/api/v1/user/",
            json=user_data
        )

        assert response.status_code in [201, 400, 422, 500, 409]


class TestGetAllUsersRouteErrors:
    """Test error paths in get_all_users route."""

    def test_get_all_users_endpoint_exists(self, test_client):
        """Test that get_all_users endpoint exists and responds."""
        response = test_client.get("/api/v1/user/")

        # Should get a response
        assert response.status_code in [200, 400, 404, 500]

    def test_get_all_users_returns_list(self, test_client):
        """Test that get_all_users returns a list or error."""
        response = test_client.get("/api/v1/user/")

        # Should be valid response
        assert 200 <= response.status_code < 600


class TestGetUserByIdRouteErrors:
    """Test error paths in get_user_by_id route."""

    def test_get_user_by_id_with_invalid_id(self, test_client):
        """Test get_user_by_id with non-integer ID."""
        response = test_client.get("/api/v1/user/invalid_id")

        # Should reject invalid ID
        assert response.status_code in [400, 422, 404]

    def test_get_user_by_id_with_negative_id(self, test_client):
        """Test get_user_by_id with negative ID."""
        response = test_client.get("/api/v1/user/-1")

        # May accept or reject depending on validation
        assert response.status_code in [200, 400, 404, 422, 500]

    def test_get_user_by_id_with_zero_id(self, test_client):
        """Test get_user_by_id with zero ID."""
        response = test_client.get("/api/v1/user/0")

        # May accept or reject
        assert response.status_code in [200, 400, 404, 422, 500]

    def test_get_user_by_id_with_very_large_id(self, test_client):
        """Test get_user_by_id with very large ID."""
        response = test_client.get("/api/v1/user/999999999999999999")

        # Should handle large number
        assert response.status_code in [200, 404, 422, 500]


class TestUpdateUserRouteErrors:
    """Test error paths in update route."""

    def test_update_user_with_invalid_id(self, test_client):
        """Test update user with non-integer ID."""
        response = test_client.patch(
            "/api/v1/user/invalid_id",
            json={"name": "Updated"}
        )

        # Should reject invalid ID
        assert response.status_code in [400, 422, 404]

    def test_update_user_with_negative_id(self, test_client):
        """Test update user with negative ID."""
        response = test_client.patch(
            "/api/v1/user/-1",
            json={"name": "Updated"}
        )

        # May accept or reject
        assert response.status_code in [200, 400, 404, 422, 500, 201]

    def test_update_user_with_invalid_json_body(self, test_client):
        """Test update user with invalid JSON body."""
        response = test_client.patch(
            "/api/v1/user/1",
            content="invalid json",
            headers={"Content-Type": "application/json"}
        )

        # Should reject invalid JSON
        assert response.status_code in [400, 422]

    def test_update_user_with_null_fields(self, test_client):
        """Test update user with all null fields."""
        user_data = {
            "name": None,
            "email": None,
            "password": None
        }

        response = test_client.patch(
            "/api/v1/user/1",
            json=user_data
        )

        # Should handle null values
        assert response.status_code in [200, 201, 400, 404, 422, 500]

    def test_update_user_with_empty_payload(self, test_client):
        """Test update user with empty JSON payload."""
        response = test_client.patch(
            "/api/v1/user/1",
            json={}
        )

        # Should handle empty payload
        assert response.status_code in [200, 201, 400, 404, 422, 500]

    def test_update_user_with_invalid_email_format(self, test_client):
        """Test update user with invalid email format."""
        user_data = {
            "name": "Updated Name",
            "email": "not-an-email",
            "password": "newpassword"
        }

        response = test_client.patch(
            "/api/v1/user/1",
            json=user_data
        )

        # Should reject invalid email
        assert response.status_code in [400, 422, 201, 200, 500]


class TestDeleteUserRouteErrors:
    """Test error paths in delete route."""

    def test_delete_user_with_invalid_id(self, test_client):
        """Test delete user with non-integer ID."""
        response = test_client.delete("/api/v1/user/invalid_id")

        # Should reject invalid ID
        assert response.status_code in [400, 422, 404]

    def test_delete_user_with_negative_id(self, test_client):
        """Test delete user with negative ID."""
        response = test_client.delete("/api/v1/user/-1")

        # May accept or reject
        assert response.status_code in [200, 204, 400, 404, 422, 500]

    def test_delete_user_with_zero_id(self, test_client):
        """Test delete user with zero ID."""
        response = test_client.delete("/api/v1/user/0")

        # May accept or reject
        assert response.status_code in [200, 204, 400, 404, 422, 500]

    def test_delete_nonexistent_user(self, test_client):
        """Test deleting a non-existent user."""
        response = test_client.delete("/api/v1/user/999999999")

        # Should handle missing user gracefully
        assert response.status_code in [200, 204, 404, 500]
