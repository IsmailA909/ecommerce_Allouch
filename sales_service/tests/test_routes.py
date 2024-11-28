import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_display_goods(client):
    response = client.get('/sales/goods')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_make_purchase(client):
    response = client.post('/sales/purchase', json={
        "customer_username": "johndoe",
        "good_id": 1,
        "quantity": 2
    })
    assert response.status_code == 201
    assert response.json['message'] == "Purchase successful"

def test_purchase_history(client):
    response = client.get('/sales/history/johndoe')
    assert response.status_code == 200
    assert isinstance(response.json, list)
