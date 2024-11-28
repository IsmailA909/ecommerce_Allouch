import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_submit_review(client):
    response = client.post('/reviews/submit', json={
        "customer_username": "johndoe",
        "good_id": 1,
        "rating": 5,
        "comment": "Excellent product!"
    })
    assert response.status_code == 201
    assert response.json['message'] == "Review submitted successfully"

def test_get_product_reviews(client):
    response = client.get('/reviews/product/1')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_moderate_review(client):
    response = client.put('/reviews/moderate/1', json={"status": "approved"})
    assert response.status_code == 200
    assert response.json['message'] == "Review status updated"
