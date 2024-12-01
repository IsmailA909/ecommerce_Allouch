from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Purchase(db.Model):
    """
    Model representing a customer purchase.

    Attributes:
    - id (int): Primary key.
    - customer_username (str): Username of the purchasing customer.
    - good_id (int): ID of the purchased good.
    - quantity (int): Quantity of the purchased good.
    - total_price (float): Total price of the purchase.
    """
    __tablename__ = 'purchases'

    id = db.Column(db.Integer, primary_key=True)
    customer_username = db.Column(db.String(50), nullable=False)
    good_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "customer_username": self.customer_username,
            "good_id": self.good_id,
            "quantity": self.quantity,
            "total_price": self.total_price
        }