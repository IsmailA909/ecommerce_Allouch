import pytest
from app import app, db

@pytest.fixture
def client():
    """Test client with in-memory SQLite database."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()  # Create all tables
        yield app.test_client()  # Provide the test client

        db.session.remove()
        db.drop_all()  # Clean up after tests
