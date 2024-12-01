import cProfile
import pstats
import io
from app import app, db

def initialize_database():
    """Initialize the database."""
    with app.app_context():
        db.create_all()

def profile_make_purchase():
    """Profile the make purchase endpoint."""
    with app.test_client() as client:
        data = {
            "customer_username": "johndoe",
            "good_id": 1,
            "quantity": 1
        }
        client.post('/sales/purchase', json=data)

if __name__ == '__main__':
    initialize_database()

    profiler = cProfile.Profile()
    profiler.enable()
