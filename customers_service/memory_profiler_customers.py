from memory_profiler import profile
from app import app

@profile
def simulate_customer_service():
    with app.test_client() as client:
        # Register a new customer
        client.post('/customers/register', json={
            "full_name": "John Doe",
            "username": "johndoe",
            "password": "password123",
            "age": 30,
            "address": "123 Elm Street",
            "gender": "Male",
            "marital_status": "Single"
        })

        # Get all customers
        client.get('/customers/all')

if __name__ == "__main__":
    simulate_customer_service()
