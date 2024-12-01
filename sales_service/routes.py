from flask import Blueprint, request, jsonify
from models import db, Purchase
import requests
import logging

"""
Routes for Sales Service
============================
Defines the API endpoints for sales operations.
"""

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

sales_bp = Blueprint('sales', __name__, url_prefix='/sales')


# Helper function to fetch data from other services
def fetch_service_data(url, method="GET", data=None):
    """
    Fetch data from another service.

    Args:
        url (str): The service URL.
        method (str): HTTP method (GET, POST, PUT).
        data (dict): Data to send with the request.

    Returns:
        dict: Response JSON or an error message.
    """
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error connecting to {url}: {e}")
        return {"error": f"Error connecting to {url}: {str(e)}"}


# 1. Display Available Goods
@sales_bp.route('/goods', methods=['GET'])
def display_goods():
    """
    Display all available goods.

    Returns:
        - 200: List of goods (name and price).
        - 500: Error message if fetching fails.
    """
    logger.info("Fetching available goods.")
    try:
        url = "http://inventory_service:5001/inventory/all"
        goods = fetch_service_data(url)
        if "error" in goods:
            logger.warning("Failed to fetch goods from Inventory Service.")
            return jsonify(goods), 500

        available_goods = [{"name": g["name"], "price": g["price"]} for g in goods]
        return jsonify(available_goods), 200
    except Exception as e:
        logger.error(f"Error fetching goods: {e}")
        return jsonify({"error": str(e)}), 500


# 2. Get Details of a Specific Good
@sales_bp.route('/goods/<int:good_id>', methods=['GET'])
def get_good_details(good_id):
    """
    Get details of a specific good.

    Args:
        good_id (int): ID of the good.

    Returns:
        - 200: Good details.
        - 404: Good not found.
        - 500: Error message if fetching fails.
    """
    logger.info(f"Fetching details for good ID {good_id}.")
    try:
        url = f"http://inventory_service:5001/inventory/{good_id}"
        good = fetch_service_data(url)
        if "error" in good:
            logger.warning(f"Good ID {good_id} not found.")
            return jsonify(good), 404
        return jsonify(good), 200
    except Exception as e:
        logger.error(f"Error fetching details for good ID {good_id}: {e}")
        return jsonify({"error": str(e)}), 500


# 3. Make a Sale
@sales_bp.route('/sale', methods=['POST'])
def make_sale():
    """
    Handle customer purchase.

    Request Body:
        - customer_username (str): Username of the purchasing customer.
        - good_id (int): ID of the good being purchased.
        - quantity (int): Quantity of the good to purchase.

    Returns:
        - 201: Success message with purchase details.
        - 400: Error if insufficient stock or wallet balance.
        - 404: Error if the customer or good is not found.
        - 500: Error for internal issues.
    """
    logger.info("Processing a new sale.")
    try:
        data = request.get_json()
        required_fields = ['customer_username', 'good_id', 'quantity']
        for field in required_fields:
            if field not in data:
                logger.warning(f"Missing required field: {field}")
                return jsonify({"error": f"'{field}' is required"}), 400

        customer_username = data['customer_username']
        good_id = data['good_id']
        quantity = data['quantity']

        # Fetch good details
        good_url = f"http://inventory_service:5001/inventory/{good_id}"
        good = fetch_service_data(good_url)
        if "error" in good:
            logger.warning(f"Good ID {good_id} not found.")
            return jsonify({"error": "Good not found"}), 404

        # Check stock availability
        if good['stock_count'] < quantity:
            logger.warning("Insufficient stock.")
            return jsonify({"error": "Insufficient stock"}), 400

        # Fetch customer wallet balance
        customer_url = f"http://customers_service:5000/customers/{customer_username}"
        customer = fetch_service_data(customer_url)
        if "error" in customer:
            logger.warning(f"Customer {customer_username} not found.")
            return jsonify({"error": "Customer not found"}), 404

        total_price = good['price'] * quantity

        # Check wallet balance
        if customer['wallet_balance'] < total_price:
            logger.warning("Insufficient wallet balance.")
            return jsonify({"error": "Insufficient wallet balance"}), 400

        # Deduct stock
        deduct_stock_url = f"http://inventory_service:5001/inventory/deduct/{good_id}"
        stock_response = fetch_service_data(
            deduct_stock_url, method="POST", data={"quantity": quantity}
        )
        if "error" in stock_response:
            logger.error("Failed to deduct stock.")
            return jsonify(stock_response), 500

        # Deduct wallet balance
        deduct_wallet_url = f"http://customers_service:5000/customers/deduct/{customer_username}"
        wallet_response = fetch_service_data(
            deduct_wallet_url, method="POST", data={"amount": total_price}
        )
        if "error" in wallet_response:
            logger.error("Failed to deduct wallet balance.")
            return jsonify(wallet_response), 500

        # Record purchase
        purchase = Purchase(
            customer_username=customer_username,
            good_id=good_id,
            quantity=quantity,
            total_price=total_price
        )
        db.session.add(purchase)
        db.session.commit()

        logger.info(f"Sale successful for customer {customer_username}.")
        return jsonify({"message": "Purchase successful", "purchase": purchase.to_dict()}), 201
    except Exception as e:
        logger.error(f"Error processing sale: {e}")
        return jsonify({"error": str(e)}), 500


# 4. Get Purchase History for a Customer
@sales_bp.route('/history/<customer_username>', methods=['GET'])
def get_purchase_history(customer_username):
    """
    Get purchase history for a customer.

    Args:
        customer_username (str): Username of the customer.

    Returns:
        - 200: List of purchases.
        - 500: Error message for internal issues.
    """
    logger.info(f"Fetching purchase history for customer {customer_username}.")
    try:
        purchases = Purchase.query.filter_by(customer_username=customer_username).all()
        return jsonify([purchase.to_dict() for purchase in purchases]), 200
    except Exception as e:
        logger.error(f"Error fetching purchase history for customer {customer_username}: {e}")
        return jsonify({"error": str(e)}), 500
