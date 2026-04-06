"""
Tests for the main application entry point.
"""
import pytest


def test_main_entry_point_import():
    """Test that main.py can be imported without errors."""
    # This test ensures the module can be imported
    try:
        import app.main  # noqa: F401
    except ImportError as e:
        pytest.fail(f"Failed to import app.main: {e}")
