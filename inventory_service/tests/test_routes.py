import pytest
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.app_context():
        with app.test_client() as client:
            yield client

def test_add_goods(client):
    """Test adding new goods to inventory."""
    with patch('models.Goods') as MockGoods, patch('models.db.session') as mock_session:
        # Mock the Goods instance
        mock_instance = MockGoods.return_value
        mock_instance.to_dict.return_value = {
            'name': 'Laptop',
            'category': 'electronics',
            'price': 900,
            'description': 'High-performance laptop',
            'stock_count': 20
        }

        # Make the POST request
        response = client.post('/inventory/add', json={
            'name': 'Laptop',
            'category': 'electronics',
            'price': 900,
            'description': 'High-performance laptop',
            'stock_count': 20
        })

        # Assertions for the response
        assert response.status_code == 201
        assert response.json['message'] == 'Goods added successfully'

        # Verify that mock_session.add was called with the correct mock_instance
        mock_session.add.assert_called_once()

        # Verify that mock_session.commit was called
        mock_session.commit.assert_called_once()

def test_get_all_goods(client):
    """Test fetching all goods."""
    with patch('models.Goods.query') as mock_query:
        mock_good = MagicMock()
        mock_good.to_dict.return_value = {
            'name': 'Laptop',
            'category': 'electronics',
            'price': 900,
            'description': 'High-performance laptop',
            'stock_count': 20
        }
        mock_query.all.return_value = [mock_good]

        response = client.get('/inventory/all')

        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['name'] == 'Laptop'
