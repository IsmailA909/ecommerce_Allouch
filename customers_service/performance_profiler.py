import cProfile
import pstats
from app import app

def profile_app():
    profiler = cProfile.Profile()
    profiler.enable()

    # Simulate requests to your service
    with app.test_client() as client:
        client.post('/customers/register', json={
            "full_name": "John Doe",
            "username": "johndoe",
            "password": "password123",
            "age": 30,
            "address": "123 Elm Street",
            "gender": "Male",
            "marital_status": "Single"
        })
        client.get('/customers/all')

    profiler.disable()
    profiler.dump_stats("performance.prof")

    # Print statistics
    stats = pstats.Stats("performance.prof")
    stats.strip_dirs()
    stats.sort_stats('cumulative')
    stats.print_stats(10)

if __name__ == "__main__":
    profile_app()
