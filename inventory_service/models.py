from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Goods(db.Model):
    """
    Model representing a good in the inventory.

    Attributes:
    - id (int): Primary key.
    - name (str): Name of the good.
    - category (str): Category of the good.
    - price (float): Price of the good.
    - description (str): Description of the good.
    - stock_count (int): Number of items in stock.
    """
    __tablename__ = 'goods'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.Enum('food', 'clothes', 'accessories', 'electronics'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    stock_count = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "description": self.description,
            "stock_count": self.stock_count,
        }
