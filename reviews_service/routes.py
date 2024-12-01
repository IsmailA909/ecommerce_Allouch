from flask import Blueprint, request, jsonify
from models import db, Review
"""
Routes for reviews Service
============================
Defines the API endpoints for review operations.
"""
reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

# Submit a review
@reviews_bp.route('/submit', methods=['POST'])
def submit_review():
    """
    Submit a review for a good.

    Request Body:
    - username (str): Username of the customer submitting the review.
    - good_id (int): ID of the reviewed good.
    - rating (int): Rating (1-5).
    - comment (str): Review comment.

    Returns:
    - 201: Success message on review submission.
    - 400: Error message if validation fails.
    """
    data = request.get_json()
    required_fields = ['customer_username', 'product_id', 'rating', 'comment']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"'{field}' is required"}), 400

    review = Review(
        customer_username=data['customer_username'],
        product_id=data['product_id'],
        rating=data['rating'],
        comment=data['comment']
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({"message": "Review submitted successfully", "review": review.to_dict()}), 201

# Update a review
@reviews_bp.route('/update/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404

    data = request.get_json()
    review.rating = data.get('rating', review.rating)
    review.comment = data.get('comment', review.comment)
    db.session.commit()
    return jsonify({"message": "Review updated", "review": review.to_dict()}), 200

# Delete a review
@reviews_bp.route('/delete/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404

    db.session.delete(review)
    db.session.commit()
    return jsonify({"message": "Review deleted successfully"}), 200

# Get all reviews for a product
@reviews_bp.route('/product/<int:product_id>', methods=['GET'])
def get_product_reviews(product_id):
    reviews = Review.query.filter_by(product_id=product_id).all()
    return jsonify([review.to_dict() for review in reviews]), 200

# Get all reviews by a customer
@reviews_bp.route('/customer/<customer_username>', methods=['GET'])
def get_customer_reviews(customer_username):
    reviews = Review.query.filter_by(customer_username=customer_username).all()
    return jsonify([review.to_dict() for review in reviews]), 200

@reviews_bp.route('/moderate/<int:review_id>', methods=['POST'])
def moderate_review(review_id):
    data = request.get_json()
    review = Review.query.get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404

    if "moderation_status" not in data:
        return jsonify({"error": "'moderation_status' is required"}), 400

    review.moderation_status = data["moderation_status"]
    db.session.commit()
    return jsonify({"message": "Review moderated successfully", "review": review.to_dict()}), 200


# Get review details
@reviews_bp.route('/<int:review_id>', methods=['GET'])
def get_review_details(review_id):
    review = Review.query.get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404

    return jsonify(review.to_dict()), 200
