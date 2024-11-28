import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_add_goods(client):
    response = client.post('/inventory/add', json={
        "name": "Laptop",
        "category": "electronics",
        "price": 1200,
        "description": "High-performance laptop",
        "stock_count": 10
    })
    assert response.status_code == 201
    assert response.json['message'] == "Goods added successfully"

def test_get_all_goods(client):
    response = client.get('/inventory/all')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_update_goods(client):
    response = client.put('/inventory/update/1', json={
        "price": 1100,
        "stock_count": 8
    })
    assert response.status_code == 200
    assert response.json['message'] == "Goods updated"
