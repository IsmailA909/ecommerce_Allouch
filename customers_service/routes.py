from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from models import db, Customer
import logging

"""
Routes for Customers Service
============================
Defines the API endpoints for customer operations.
"""

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

customers_bp = Blueprint('customers', __name__, url_prefix='/customers')

# Register a new customer
@customers_bp.route('/register', methods=['POST'])
def register_customer():
    """
    Register a new customer.

    Request Body:
    - full_name (str): The full name of the customer.
    - username (str): A unique username for the customer.
    - password (str): The password for the customer account.
    - age (int): Age of the customer.
    - address (str): Address of the customer.
    - gender (str): Gender of the customer.
    - marital_status (str): Marital status of the customer.

    Returns:
    - 201: Success message on successful registration.
    - 400: Error message if username already exists or validation fails.
    """    
    logger.info("Attempting to register a new customer.")
    data = request.get_json()
    if not data:
        logger.warning("Invalid input received for customer registration.")
        return jsonify({"error": "Invalid input"}), 400

    required_fields = ['full_name', 'username', 'password', 'age', 'address', 'gender', 'marital_status']
    for field in required_fields:
        if field not in data:
            logger.warning(f"Missing required field: {field}")
            return jsonify({"error": f"'{field}' is required"}), 400

    if Customer.query.filter_by(username=data['username']).first():
        logger.warning(f"Username '{data['username']}' already exists.")
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
    logger.info(f"Customer '{data['username']}' registered successfully.")
    return jsonify({"message": "Customer registered successfully"}), 201


# Delete a customer
@customers_bp.route('/delete/<username>', methods=['DELETE'])
def delete_customer(username):
    logger.info(f"Attempting to delete customer '{username}'.")
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        logger.warning(f"Customer '{username}' not found.")
        return jsonify({"error": "Customer not found"}), 404
    db.session.delete(customer)
    db.session.commit()
    logger.info(f"Customer '{username}' deleted successfully.")
    return jsonify({"message": "Customer deleted successfully"}), 200


# Update customer information
@customers_bp.route('/update/<username>', methods=['PUT'])
def update_customer(username):
    logger.info(f"Attempting to update customer '{username}'.")
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        logger.warning(f"Customer '{username}' not found.")
        return jsonify({"error": "Customer not found"}), 404

    data = request.get_json()
    for key, value in data.items():
        if hasattr(customer, key):
            setattr(customer, key, value)
    db.session.commit()
    logger.info(f"Customer '{username}' updated successfully.")
    return jsonify({"message": "Customer updated successfully"}), 200


# Get all customers
@customers_bp.route('/all', methods=['GET'])
def get_all_customers():
    logger.info("Fetching all customers.")
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers]), 200


# Get a customer by username
@customers_bp.route('/<username>', methods=['GET'])
def get_customer_by_username(username):
    logger.info(f"Fetching customer '{username}'.")
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        logger.warning(f"Customer '{username}' not found.")
        return jsonify({"error": "Customer not found"}), 404
    return jsonify(customer.to_dict()), 200


# Charge wallet
@customers_bp.route('/charge/<username>', methods=['POST'])
def charge_wallet(username):
    logger.info(f"Attempting to charge wallet for customer '{username}'.")
    data = request.get_json()
    amount = data.get('amount')
    if not amount or amount <= 0:
        logger.warning("Invalid amount provided for wallet charge.")
        return jsonify({"error": "Invalid amount"}), 400

    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        logger.warning(f"Customer '{username}' not found.")
        return jsonify({"error": "Customer not found"}), 404

    customer.wallet_balance += amount
    db.session.commit()
    logger.info(f"Wallet charged for customer '{username}'. New balance: {customer.wallet_balance}.")
    return jsonify({"message": "Wallet charged", "wallet_balance": customer.wallet_balance}), 200


# Deduct from wallet
@customers_bp.route('/deduct/<username>', methods=['POST'])
def deduct_wallet(username):
    logger.info(f"Attempting to deduct wallet for customer '{username}'.")
    data = request.get_json()
    amount = data.get('amount')
    if not amount or amount <= 0:
        logger.warning("Invalid amount provided for wallet deduction.")
        return jsonify({"error": "Invalid amount"}), 400

    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        logger.warning(f"Customer '{username}' not found.")
        return jsonify({"error": "Customer not found"}), 404

    if customer.wallet_balance < amount:
        logger.warning(f"Insufficient balance for customer '{username}'.")
        return jsonify({"error": "Insufficient balance"}), 400

    customer.wallet_balance -= amount
    db.session.commit()
    logger.info(f"Wallet deducted for customer '{username}'. New balance: {customer.wallet_balance}.")
    return jsonify({"message": "Wallet deducted", "wallet_balance": customer.wallet_balance}), 200
