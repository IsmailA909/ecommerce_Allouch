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

@customers_bp.route('/status', methods=['GET'])
def health_check():
    """
    Health Check for Customers Service

    Returns:
    - 200: JSON response indicating the service is healthy.
    """
    return jsonify({"status": "Service is healthy"}), 200

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

    # Minimal validation for specific fields
    if len(data['password']) < 8:
        logger.warning("Password length is less than 8 characters.")
        return jsonify({"error": "Password must be at least 8 characters long"}), 400

    if not isinstance(data['age'], int) or data['age'] <= 0:
        logger.warning("Invalid age provided.")
        return jsonify({"error": "Age must be a positive integer"}), 400

    if data['gender'] not in ['male', 'female', 'other']:
        logger.warning("Invalid gender provided.")
        return jsonify({"error": "Gender must be 'male', 'female', or 'other'"}), 400

    if len(data['username']) < 3:
        logger.warning("Username length is less than 3 characters.")
        return jsonify({"error": "Username must be at least 3 characters long"}), 400

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
    """
    Delete an existing customer.

    Parameters:
    - username (str): The username of the customer to delete.

    Returns:
    - 200: Success message if deletion was successful.
    - 404: Error message if the customer was not found.
    """
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
    """
    Update information of an existing customer.

    Parameters:
    - username (str): The username of the customer to update.

    Request Body:
    - Any field(s) from the customer model.

    Returns:
    - 200: Success message and updated customer information.
    - 404: Error message if the customer was not found.
    """
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
    """
    Retrieve all registered customers.

    Returns:
    - 200: List of all customers.
    """
    logger.info("Fetching all customers.")
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers]), 200


# Get a customer by username
@customers_bp.route('/get/<username>', methods=['GET'])
def get_customer_by_username(username):
    """
    Retrieve customer information by username.

    Parameters:
    - username (str): The username of the customer.

    Returns:
    - 200: Customer information.
    - 404: Error message if the customer was not found.
    """
    logger.info(f"Fetching customer '{username}'.")
    customer = Customer.query.filter_by(username=username).first()
    if not customer:
        logger.warning(f"Customer '{username}' not found.")
        return jsonify({"error": "Customer not found"}), 404
    return jsonify(customer.to_dict()), 200


# Charge wallet
@customers_bp.route('/charge/<username>', methods=['POST'])
def charge_wallet(username):
    """
    Add funds to a customer's wallet.

    Parameters:
    - username (str): The username of the customer.

    Request Body:
    - amount (float): Amount to be added.

    Returns:
    - 200: Success message and updated wallet balance.
    - 400: Error message if validation fails.
    - 404: Error message if the customer was not found.
    """
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
    """
    Deduct funds from a customer's wallet.

    Parameters:
    - username (str): The username of the customer.

    Request Body:
    - amount (float): Amount to be deducted.

    Returns:
    - 200: Success message and updated wallet balance.
    - 400: Error message if validation fails or insufficient funds.
    - 404: Error message if the customer was not found.
    """
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
