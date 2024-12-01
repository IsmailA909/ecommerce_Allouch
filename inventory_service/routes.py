from flask import Blueprint, request, jsonify
from models import db, Goods
import logging

"""
Routes for Inventory Service
============================
Defines the API endpoints for inventory operations.
"""

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

# Add new goods
@inventory_bp.route('/add', methods=['POST'])
def add_goods():
    """
    Add new goods to the inventory.

    Request Body:
    - name (str): Name of the good.
    - category (str): Category (e.g., food, electronics).
    - price (float): Price of the good.
    - description (str): Brief description of the good.
    - stock_count (int): Initial stock count.

    Returns:
    - 201: Success message and details of the added good.
    - 400: Error message if required fields are missing.
    """
    logger.info("Attempting to add new goods to inventory.")
    data = request.get_json()
    required_fields = ['name', 'category', 'price', 'description', 'stock_count']
    for field in required_fields:
        if field not in data:
            logger.warning(f"Missing required field: {field}")
            return jsonify({"error": f"'{field}' is required"}), 400

    goods = Goods(
        name=data['name'],
        category=data['category'],
        price=data['price'],
        description=data['description'],
        stock_count=data['stock_count'],
    )
    db.session.add(goods)
    db.session.commit()
    logger.info(f"Goods '{data['name']}' added successfully to inventory.")
    return jsonify({"message": "Goods added successfully", "goods": goods.to_dict()}), 201


# Get details of a specific good
@inventory_bp.route('/<int:goods_id>', methods=['GET'])
def get_good_details(goods_id):
    logger.info(f"Fetching details for goods ID {goods_id}.")
    goods = Goods.query.get(goods_id)
    if not goods:
        logger.warning(f"Goods with ID {goods_id} not found.")
        return jsonify({"error": "Good not found"}), 404

    return jsonify(goods.to_dict()), 200


# Deduct goods from inventory
@inventory_bp.route('/deduct/<int:goods_id>', methods=['POST'])
def deduct_goods(goods_id):
    logger.info(f"Attempting to deduct goods ID {goods_id} from inventory.")
    data = request.get_json()
    quantity = data.get('quantity', 0)

    goods = Goods.query.get(goods_id)
    if not goods:
        logger.warning(f"Goods with ID {goods_id} not found.")
        return jsonify({"error": "Goods not found"}), 404

    if goods.stock_count < quantity:
        logger.warning(f"Insufficient stock for goods ID {goods_id}. Requested: {quantity}, Available: {goods.stock_count}.")
        return jsonify({"error": "Insufficient stock"}), 400

    goods.stock_count -= quantity
    db.session.commit()
    logger.info(f"Stock updated for goods ID {goods_id}. Remaining stock: {goods.stock_count}.")
    return jsonify({"message": "Stock updated", "goods": goods.to_dict()}), 200


# Update goods information
@inventory_bp.route('/update/<int:goods_id>', methods=['PUT'])
def update_goods(goods_id):
    logger.info(f"Attempting to update goods ID {goods_id}.")
    goods = Goods.query.get(goods_id)
    if not goods:
        logger.warning(f"Goods with ID {goods_id} not found.")
        return jsonify({"error": "Goods not found"}), 404

    data = request.get_json()
    for key, value in data.items():
        if hasattr(goods, key):
            setattr(goods, key, value)
    db.session.commit()
    logger.info(f"Goods ID {goods_id} updated successfully.")
    return jsonify({"message": "Goods updated", "goods": goods.to_dict()}), 200


# Get all goods
@inventory_bp.route('/all', methods=['GET'])
def get_all_goods():
    logger.info("Fetching all goods from inventory.")
    goods_list = Goods.query.all()
    return jsonify([goods.to_dict() for goods in goods_list]), 200
