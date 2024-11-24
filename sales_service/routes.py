from flask import Blueprint, request, jsonify
from models import db, Purchase
import requests

sales_bp = Blueprint('sales', __name__, url_prefix='/sales')

# Helper function to fetch data from other services
def fetch_service_data(url, method="GET", data=None):
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        response.raise_for_status()  # Raise an error for bad HTTP responses
        return response.json()
    except Exception as e:
        return {"error": f"Error connecting to {url}: {str(e)}"}

# 1. Display Available Goods
@sales_bp.route('/goods', methods=['GET'])
def display_goods():
    try:
        url = "http://inventory_service:5001/inventory/all"
        goods = fetch_service_data(url)
        if "error" in goods:
            return jsonify(goods), 500

        # Only return name and price
        available_goods = [{"name": g["name"], "price": g["price"]} for g in goods]
        return jsonify(available_goods), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 2. Get Details of a Specific Good
@sales_bp.route('/goods/<int:good_id>', methods=['GET'])
def get_good_details(good_id):
    try:
        url = f"http://inventory_service:5001/inventory/{good_id}"
        good = fetch_service_data(url)
        if "error" in good:
            return jsonify(good), 404
        return jsonify(good), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. Make a Sale
@sales_bp.route('/sale', methods=['POST'])
def make_sale():
    try:
        data = request.get_json()
        customer_username = data.get('customer_username')
        good_id = data.get('good_id')
        quantity = data.get('quantity')

        # Fetch good details
        good_url = f"http://inventory_service:5001/inventory/{good_id}"
        good = fetch_service_data(good_url)
        if "error" in good:
            return jsonify({"error": "Good not found"}), 404

        # Check stock availability
        if good['stock_count'] < quantity:
            return jsonify({"error": "Insufficient stock"}), 400

        # Fetch customer wallet balance
        customer_url = f"http://customers_service:5000/customers/{customer_username}"
        customer = fetch_service_data(customer_url)
        if "error" in customer:
            return jsonify({"error": "Customer not found"}), 404

        total_price = good['price'] * quantity

        # Check wallet balance
        if customer['wallet_balance'] < total_price:
            return jsonify({"error": "Insufficient wallet balance"}), 400

        # Deduct stock
        deduct_stock_url = f"http://inventory_service:5001/inventory/deduct/{good_id}"
        stock_response = fetch_service_data(
            deduct_stock_url, method="POST", data={"quantity": quantity}
        )
        if "error" in stock_response:
            return jsonify(stock_response), 500

        # Deduct wallet balance
        deduct_wallet_url = f"http://customers_service:5000/customers/deduct/{customer_username}"
        wallet_response = fetch_service_data(
            deduct_wallet_url, method="POST", data={"amount": total_price}
        )
        if "error" in wallet_response:
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

        return jsonify({"message": "Purchase successful", "purchase": purchase.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 4. Get Purchase History for a Customer
@sales_bp.route('/history/<customer_username>', methods=['GET'])
def get_purchase_history(customer_username):
    try:
        purchases = Purchase.query.filter_by(customer_username=customer_username).all()
        return jsonify([purchase.to_dict() for purchase in purchases]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
