import cProfile
import pstats
import io
from app import app, db

def initialize_database():
    """Initialize the database."""
    with app.app_context():
        db.create_all()

def profile_add_goods():
    """Profile the add goods endpoint."""
    with app.test_client() as client:
        data = {
            "name": "Laptop",
            "category": "electronics",
            "price": 1200,
            "description": "High-performance laptop",
            "stock_count": 10
        }
        client.post('/inventory/add', json=data)

if __name__ == '__main__':
    initialize_database()

    profiler = cProfile.Profile()
    profiler.enable()
    profile_add_goods()
    profiler.disable()

    # Output profiling results
    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.strip_dirs()
    stats.sort_stats('cumulative')
    stats.print_stats()
    print(stream.getvalue())
