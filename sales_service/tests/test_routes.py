import pytest
from unittest.mock import patch, MagicMock
from app import app



def test_display_goods(client):
    """Test displaying available goods."""
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = [
            {'name': 'Laptop', 'price': 900}
        ]
        response = client.get('/sales/goods')
        assert response.status_code == 200
        assert response.json[0]['name'] == 'Laptop'


