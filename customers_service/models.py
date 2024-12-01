from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    """
    Model representing a customer.

    Attributes:
    - id (int): Primary key.
    - full_name (str): Full name of the customer.
    - username (str): Unique username.
    - password (str): Hashed password for the customer.
    - age (int): Age of the customer.
    - address (str): Address of the customer.
    - gender (str): Gender of the customer.
    - marital_status (str): Marital status of the customer.
    - wallet_balance (float): Current wallet balance.
    """
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.Text, nullable=False)
    gender = db.Column(db.Enum('Male', 'Female', 'Other'), nullable=False)
    marital_status = db.Column(db.Enum('Single', 'Married', 'Divorced', 'Widowed'), nullable=False)
    wallet_balance = db.Column(db.Float, default=0.0)

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "username": self.username,
            "age": self.age,
            "address": self.address,
            "gender": self.gender,
            "marital_status": self.marital_status,
            "wallet_balance": self.wallet_balance,
        }
