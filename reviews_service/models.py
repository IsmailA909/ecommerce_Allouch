from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_username = db.Column(db.String(50), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="pending")  # pending/approved/flagged

    def to_dict(self):
        return {
            "id": self.id,
            "customer_username": self.customer_username,
            "product_id": self.product_id,
            "rating": self.rating,
            "comment": self.comment,
            "status": self.status
        }