import cProfile
import pstats
import io
from app import app, db

def initialize_database():
    """Initialize the database."""
    with app.app_context():
        db.create_all()

def profile_submit_review():
    """Profile the submit review endpoint."""
    with app.test_client() as client:
        data = {
            "customer_username": "johndoe",
            "product_id": 1,
            "rating": 5,
            "comment": "Excellent product!"
        }
        client.post('/reviews/submit', json=data)

if __name__ == '__main__':
    initialize_database()

    profiler = cProfile.Profile()
    profiler.enable()
    profile_submit_review()
    profiler.disable()

    # Output profiling results
    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.strip_dirs()
    stats.sort_stats('cumulative')
    stats.print_stats()
    print(stream.getvalue())
