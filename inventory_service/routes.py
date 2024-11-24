from flask import Blueprint, request, jsonify
from models import db, Goods

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

# Add new goods
@inventory_bp.route('/add', methods=['POST'])
def add_goods():
    data = request.get_json()
    required_fields = ['name', 'category', 'price', 'description', 'stock_count']
    for field in required_fields:
        if field not in data:
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
    return jsonify({"message": "Goods added successfully", "goods": goods.to_dict()}), 201

# Get details of a specific good
@inventory_bp.route('/<int:goods_id>', methods=['GET'])
def get_good_details(goods_id):
    goods = Goods.query.get(goods_id)
    if not goods:
        return jsonify({"error": "Good not found"}), 404

    return jsonify(goods.to_dict()), 200



# Deduct goods from inventory
@inventory_bp.route('/deduct/<int:goods_id>', methods=['POST'])
def deduct_goods(goods_id):
    data = request.get_json()
    quantity = data.get('quantity', 0)

    goods = Goods.query.get(goods_id)
    if not goods:
        return jsonify({"error": "Goods not found"}), 404

    if goods.stock_count < quantity:
        return jsonify({"error": "Insufficient stock"}), 400

    goods.stock_count -= quantity
    db.session.commit()
    return jsonify({"message": "Stock updated", "goods": goods.to_dict()}), 200


# Update goods information
@inventory_bp.route('/update/<int:goods_id>', methods=['PUT'])
def update_goods(goods_id):
    goods = Goods.query.get(goods_id)
    if not goods:
        return jsonify({"error": "Goods not found"}), 404

    data = request.get_json()
    for key, value in data.items():
        if hasattr(goods, key):
            setattr(goods, key, value)
    db.session.commit()
    return jsonify({"message": "Goods updated", "goods": goods.to_dict()}), 200


# Get all goods
@inventory_bp.route('/all', methods=['GET'])
def get_all_goods():
    goods_list = Goods.query.all()
    return jsonify([goods.to_dict() for goods in goods_list]), 200
