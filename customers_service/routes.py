from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models import db, Customer

customers_bp = Blueprint('customers', __name__, url_prefix='/customers')

# Register a new customer
@customers_bp.route('/register', methods=['POST'])
def register_customer():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400

    required_fields = ['full_name', 'username', 'password', 'age', 'address', 'gender', 'marital_status']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    if Customer.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 400

    hashed_password = generate_password_hash(data['password'])
    customer = Customer(
        full_name=data['full_name'],
        username=data['username'],
        password=hashed_password,
        age=data['age'],
        address=data['address'],
        gender=data['gender'],
        marital_status=data['marital_status'],
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify({"message": "Customer registered successfully"}), 201


# Delete a customer
@customers_bp.route('/delete/<username>', methods=['DELETE'])
def delete_customer(username):
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted successfully"}), 200


# Update customer information
@customers_bp.route('/update/<username>', methods=['PUT'])
def update_customer(username):
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    data = request.get_json()
    for key, value in data.items():
        if hasattr(customer, key):
            setattr(customer, key, value)
    db.session.commit()
    return jsonify({"message": "Customer updated successfully"}), 200


# Get all customers
@customers_bp.route('/all', methods=['GET'])
def get_all_customers():
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers]), 200


# Get a customer by username
@customers_bp.route('/<username>', methods=['GET'])
def get_customer_by_username(username):
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify(customer.to_dict()), 200


# Charge wallet
@customers_bp.route('/charge/<username>', methods=['POST'])
def charge_wallet(username):
    data = request.get_json()
    amount = data.get('amount')
    if not amount or amount <= 0:
        return jsonify({"error": "Invalid amount"}), 400

    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    customer.wallet_balance += amount
    db.session.commit()
    return jsonify({"message": "Wallet charged", "wallet_balance": customer.wallet_balance}), 200


# Deduct from wallet
@customers_bp.route('/deduct/<username>', methods=['POST'])
def deduct_wallet(username):
    data = request.get_json()
    amount = data.get('amount')
    if not amount or amount <= 0:
        return jsonify({"error": "Invalid amount"}), 400

    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404

    if customer.wallet_balance < amount:
        return jsonify({"error": "Insufficient balance"}), 400

    customer.wallet_balance -= amount
    db.session.commit()
    return jsonify({"message": "Wallet deducted", "wallet_balance": customer.wallet_balance}), 200
