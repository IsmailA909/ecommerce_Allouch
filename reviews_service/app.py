from flask import Flask
from models import db
from routes import reviews_bp
"""
reviews Service Module
========================
Handles review-related operations.
"""
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:userpass@ecommerce_db/ecommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)

# Create tables if not exist
with app.app_context():
    db.create_all()

# Register blueprint
app.register_blueprint(reviews_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
