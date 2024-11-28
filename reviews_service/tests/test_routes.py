import pytest
from app import app, db
from models import Review


@pytest.fixture
def client():
    """Test client setup with in-memory database."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory SQLite database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()  # Create tables

        # Seed test data
        review = Review(product_id=1, username='test_user', rating=5, comment='Great product!')
        db.session.add(review)
        db.session.commit()

        with app.test_client() as client:
            yield client

        db.session.remove()
        db.drop_all()  # Clean up after tests


def test_submit_review(client):
    """Test submitting a review."""
    response = client.post('/reviews/submit', json={
        "product_id": 1,
        "username": "test_user",
        "rating": 5,
        "comment": "Amazing product!"
    })

    assert response.status_code == 201
    assert response.json["message"] == "Review submitted successfully"


def test_get_product_reviews(client):
    """Test retrieving reviews for a specific product."""
    # Add a review to the database
    response = client.post('/reviews/submit', json={
        "product_id": 1,
        "username": "test_user",
        "rating": 5,
        "comment": "Amazing product!"
    })

    # Get reviews for the product
    response = client.get('/reviews/product/1')
    assert response.status_code == 200
    assert len(response.json) > 0
    assert response.json[0]["comment"] == "Amazing product!"


def test_delete_review(client):
    """Test deleting a review."""
    # Add a review
    response = client.post('/reviews/submit', json={
        "product_id": 1,
        "username": "test_user",
        "rating": 5,
        "comment": "Amazing product!"
    })

    review_id = response.json["review"]["id"]

    # Delete the review
    response = client.delete(f'/reviews/delete/{review_id}')
    assert response.status_code == 200
    assert response.json["message"] == "Review deleted successfully"
