from flask import Blueprint, request, jsonify
from models import db, Review
import logging

"""
Routes for Reviews Service
============================
Defines the API endpoints for review operations.
"""

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

@reviews_bp.route('/status', methods=['GET'])
def health_check():
    """
    Status Check for Reviews Service.

    Returns:
    - 200: If the service is running.
    """
    return jsonify({"status": "Reviews Service is healthy"}), 200


# Submit a review
@reviews_bp.route('/submit', methods=['POST'])
def submit_review():
    """
    Submit a review for a product.

    Request Body:
    - customer_username (str): Username of the customer submitting the review.
    - product_id (int): ID of the reviewed product.
    - rating (int): Rating (1-5).
    - comment (str): Review comment.

    Returns:
    - 201: Success message on review submission.
    - 400: Error message if validation fails.
    """
    logger.info("Submitting a new review.")
    data = request.get_json()

    # Validate input fields
    required_fields = ['customer_username', 'product_id', 'rating', 'comment']
    for field in required_fields:
        if field not in data:
            logger.warning(f"Missing required field: {field}")
            return jsonify({"error": f"'{field}' is required"}), 400

    if not (1 <= data['rating'] <= 5):
        logger.warning("Invalid rating provided.")
        return jsonify({"error": "Rating must be between 1 and 5"}), 400

    review = Review(
        customer_username=data['customer_username'],
        product_id=data['product_id'],
        rating=data['rating'],
        comment=data['comment']
    )
    db.session.add(review)
    db.session.commit()
    logger.info(f"Review submitted successfully for product ID {data['product_id']}.")
    return jsonify({"message": "Review submitted successfully", "review": review.to_dict()}), 201


# Update a review
@reviews_bp.route('/update/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    logger.info(f"Updating review ID {review_id}.")
    review = Review.query.get(review_id)
    if not review:
        logger.warning(f"Review ID {review_id} not found.")
        return jsonify({"error": "Review not found"}), 404

    data = request.get_json()
    if "rating" in data and not (1 <= data["rating"] <= 5):
        logger.warning("Invalid rating provided for update.")
        return jsonify({"error": "Rating must be between 1 and 5"}), 400

    review.rating = data.get('rating', review.rating)
    review.comment = data.get('comment', review.comment)
    db.session.commit()
    logger.info(f"Review ID {review_id} updated successfully.")
    return jsonify({"message": "Review updated successfully", "review": review.to_dict()}), 200


# Delete a review
@reviews_bp.route('/delete/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    logger.info(f"Deleting review ID {review_id}.")
    review = Review.query.get(review_id)
    if not review:
        logger.warning(f"Review ID {review_id} not found.")
        return jsonify({"error": "Review not found"}), 404

    db.session.delete(review)
    db.session.commit()
    logger.info(f"Review ID {review_id} deleted successfully.")
    return jsonify({"message": "Review deleted successfully"}), 200


# Get all reviews for a product
@reviews_bp.route('/product/<int:product_id>', methods=['GET'])
def get_product_reviews(product_id):
    logger.info(f"Fetching all reviews for product ID {product_id}.")
    reviews = Review.query.filter_by(product_id=product_id).all()
    return jsonify([review.to_dict() for review in reviews]), 200


# Get all reviews by a customer
@reviews_bp.route('/customer/get/<customer_username>', methods=['GET'])
def get_customer_reviews(customer_username):
    logger.info(f"Fetching all reviews by customer {customer_username}.")
    reviews = Review.query.filter_by(customer_username=customer_username).all()
    return jsonify([review.to_dict() for review in reviews]), 200


# Moderate a review
@reviews_bp.route('/moderate/<int:review_id>', methods=['POST'])
def moderate_review(review_id):
    logger.info(f"Moderating review ID {review_id}.")
    data = request.get_json()
    review = Review.query.get(review_id)
    if not review:
        logger.warning(f"Review ID {review_id} not found.")
        return jsonify({"error": "Review not found"}), 404

    if "moderation_status" not in data:
        logger.warning("Moderation status not provided.")
        return jsonify({"error": "'moderation_status' is required"}), 400

    review.moderation_status = data["moderation_status"]
    db.session.commit()
    logger.info(f"Review ID {review_id} moderated successfully.")
    return jsonify({"message": "Review moderated successfully", "review": review.to_dict()}), 200


# Get review details
@reviews_bp.route('/<int:review_id>', methods=['GET'])
def get_review_details(review_id):
    logger.info(f"Fetching details for review ID {review_id}.")
    review = Review.query.get(review_id)
    if not review:
        logger.warning(f"Review ID {review_id} not found.")
        return jsonify({"error": "Review not found"}), 404

    return jsonify(review.to_dict()), 200
