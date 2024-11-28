import pytest
from app import app as flask_app

@pytest.fixture
def app():
    """Fixture for the Flask application."""
    yield flask_app

@pytest.fixture
def client(app):
    """Fixture for the Flask test client."""
    return app.test_client()
