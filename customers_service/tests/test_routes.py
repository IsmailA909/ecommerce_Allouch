import pytest
from unittest.mock import patch, MagicMock
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.app_context():  # Push application context
        with app.test_client() as client:
            yield client


def test_register_customer(client):
    """Test customer registration."""
    with patch('models.Customer.query') as mock_query, patch('models.Customer') as MockCustomer, patch('models.db.session') as mock_session:
        # Simulate username not existing
        mock_query.filter_by.return_value.first.return_value = None

        # Mock the Customer instance
        mock_instance = MockCustomer.return_value
        mock_instance.to_dict.return_value = {
            'full_name': 'John Doe',
            'username': 'johndoe',
            'age': 30,
            'address': '123 Elm Street',
            'gender': 'Male',
            'marital_status': 'Single',
            'wallet_balance': 0.0
        }

        # Mock session behavior
        mock_session.add.return_value = None
        mock_session.commit.return_value = None

        # Make the POST request
        response = client.post('/customers/register', json={
            'full_name': 'John Doe',
            'username': 'johndoe',
            'password': 'password123',
            'age': 30,
            'address': '123 Elm Street',
            'gender': 'Male',
            'marital_status': 'Single'
        })

        # Assert response
        assert response.status_code == 201
        assert response.json['message'] == 'Customer registered successfully'


def test_register_customer_username_exists(client):
    """Test customer registration with an existing username."""
    with patch('models.Customer.query') as mock_query:
        # Simulate username already existing
        mock_query.filter_by.return_value.first.return_value = MagicMock()

        # Make the POST request
        response = client.post('/customers/register', json={
            'full_name': 'John Doe',
            'username': 'johndoe',  # Existing username
            'password': 'password123',
            'age': 30,
            'address': '123 Elm Street',
            'gender': 'Male',
            'marital_status': 'Single'
        })

        # Assert response
        assert response.status_code == 400
        assert response.json['error'] == 'Username already exists'


def test_get_all_customers(client):
    with patch('models.Customer.query') as mock_query:
        # Mock Query Result
        mock_customer = MagicMock()
        mock_customer.to_dict.return_value = {
            'full_name': 'John Doe',
            'username': 'johndoe',
            'age': 30,
            'address': '123 Elm Street',
            'gender': 'Male',
            'marital_status': 'Single',
            'wallet_balance': 0.0
        }
        mock_query.all.return_value = [mock_customer]

        # Send request
        response = client.get('/customers/all')

        # Assert response
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['full_name'] == 'John Doe'


def test_get_customer(client):
    with patch('models.Customer.query') as mock_query:
        # Mock Query Result
        mock_customer = MagicMock()
        mock_customer.to_dict.return_value = {
            'full_name': 'John Doe',
            'username': 'johndoe',
            'age': 30,
            'address': '123 Elm Street',
            'gender': 'Male',
            'marital_status': 'Single',
            'wallet_balance': 0.0
        }
        mock_query.filter_by.return_value.first.return_value = mock_customer

        # Send request
        response = client.get('/customers/johndoe')

        # Assert response
        assert response.status_code == 200
        assert response.json['full_name'] == 'John Doe'
