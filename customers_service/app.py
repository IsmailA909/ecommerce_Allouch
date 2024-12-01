from flask import Flask
from models import db
from routes import customers_bp
"""
Customers Service Module
========================
Handles customer-related operations such as registration, deletion, and updates.
"""
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:userpass@ecommerce_db/ecommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)

# Ensure database schema is created at startup
with app.app_context():
    try:
        db.create_all()
        print("Database schema initialized successfully.")
    except Exception as e:
        print(f"Error initializing database schema: {e}")

# Register blueprint
app.register_blueprint(customers_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
