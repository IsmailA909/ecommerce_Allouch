from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Purchase(db.Model):
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