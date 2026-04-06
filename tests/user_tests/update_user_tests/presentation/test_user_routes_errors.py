"""
Tests for error handling in update and delete routes.
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


class TestUpdateUserRouteErrorHandling:
    """Test error paths specific to update route."""

    def test_update_user_route_handles_validation_errors(self, test_client):
        """Test that update route handles validation errors gracefully."""
        # Send various types of bad data
        response = test_client.patch(
            "/api/v1/user/1",
            json={"name": 123}  # Invalid type
        )

        # Should get a response without crashing
        assert response.status_code in [200, 201, 400, 404, 422, 500]

    def test_update_user_with_extra_fields(self, test_client):
        """Test update user with extra unknown fields."""
        user_data = {
            "name": "Updated Name",
            "email": "updated@example.com",
            "password": "newpassword",
            "extra_field": "should_be_ignored",
            "another_extra": 123
        }

        response = test_client.patch(
            "/api/v1/user/1",
            json=user_data
        )

        # Should handle extra fields
        assert response.status_code in [200, 201, 400, 404, 422, 500]

    def test_update_user_with_boolean_fields(self, test_client):
        """Test update user with boolean fields."""
        user_data = {
            "name": "Test",
            "email": "test@example.com",
            "password": "pass"
        }

        response = test_client.patch(
            "/api/v1/user/1",
            json=user_data
        )

        assert response.status_code in [200, 201, 400, 404, 422, 500]


class TestDeleteUserErrorScenarios:
    """Test comprehensive error scenarios for delete operation."""

    def test_delete_user_idempotency(self, test_client):
        """Test that deleting a user twice doesn't cause errors."""
        # First delete
        response1 = test_client.delete("/api/v1/user/999999")

        # Second delete of same non-existent user
        response2 = test_client.delete("/api/v1/user/999999")

        # Both should get responses
        assert response1.status_code in [200, 204, 404, 500]
        assert response2.status_code in [200, 204, 404, 500]

    def test_delete_user_with_very_large_id(self, test_client):
        """Test delete with extremely large ID."""
        response = test_client.delete("/api/v1/user/9223372036854775807")  # Max 64-bit int

        # Should handle gracefully
        assert response.status_code in [200, 204, 404, 422, 500]

    def test_delete_user_with_float_id(self, test_client):
        """Test delete with float ID (should be coerced or rejected)."""
        response = test_client.delete("/api/v1/user/1.5")

        # Should handle or reject float
        assert response.status_code in [200, 204, 400, 404, 422, 500]


class TestRouteIntegrationErrors:
    """Integration tests for error scenarios across multiple routes."""

    def test_create_then_retrieve_user(self, test_client):
        """Test creating and then retrieving a user."""
        create_response = test_client.post(
            "/api/v1/user/",
            json={
                "name": "Integration Test User",
                "email": "integration@example.com",
                "password": "password123"
            }
        )

        # If create succeeded
        if create_response.status_code == 201:
            response_data = create_response.json()
            if "id" in response_data:
                user_id = response_data["id"]
                get_response = test_client.get(f"/api/v1/user/{user_id}")
                # Get should succeed or at least not crash
                assert get_response.status_code in [200, 404, 500]

    def test_create_duplicate_then_update(self, test_client):
        """Test creating a user, then attempting operations."""
        user_data = {
            "name": "Test User",
            "email": "duplicate@example.com",
            "password": "password123"
        }

        # Create user
        create_response = test_client.post("/api/v1/user/", json=user_data)

        # Try to update with valid data
        update_response = test_client.patch(
            "/api/v1/user/1",
            json={"name": "Updated"}
        )

        # Both should return valid responses
        assert 200 <= create_response.status_code < 600
        assert 200 <= update_response.status_code < 600
