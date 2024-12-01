import cProfile
import pstats
import io
from app import app, db

def initialize_database():
    """Initialize the database."""
    with app.app_context():
        db.create_all()

def profile_customer_registration():
    """Profile the customer registration endpoint."""
    with app.test_client() as client:
        data = {
            "full_name": "John Doe",
            "username": "johndoe",
            "password": "securepass",
            "age": 30,
            "address": "123 Elm Street",
            "gender": "Male",
            "marital_status": "Single"
        }
        client.post('/customers/register', json=data)

if __name__ == '__main__':
    initialize_database()

    profiler = cProfile.Profile()
    profiler.enable()
    profile_customer_registration()
    profiler.disable()

    # Output profiling results
    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.strip_dirs()
    stats.sort_stats('cumulative')
    stats.print_stats()
    print(stream.getvalue())
