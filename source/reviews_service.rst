Reviews Service
===============

The Reviews Service enables customers to submit, update, and delete product reviews. It also allows administrators to moderate reviews to maintain the integrity of feedback.

Key Responsibilities
---------------------
- **Submit Reviews:** Allows customers to provide feedback on products with a rating and comment.
- **Update Reviews:** Enables customers to modify their existing reviews.
- **Delete Reviews:** Allows customers and administrators to remove reviews.
- **Moderate Reviews:** Lets administrators approve or flag reviews.
- **Retrieve Reviews:** Retrieves reviews for a specific product or customer.

Available Endpoints
--------------------

1. **Submit Review**
   - **Method:** POST
   - **URL:** `/reviews/submit`
   - **Description:** Submits a new review for a product.
   - **Payload:**
     ::

       {
         "customer_username": "johndoe",
         "good_id": 1,
         "rating": 5,
         "comment": "Great product!"
       }
   - **Response:**
     ::

       {
         "message": "Review submitted successfully"
       }

2. **Update Review**
   - **Method:** PUT
   - **URL:** `/reviews/update/<int:review_id>`
   - **Description:** Updates an existing review.
   - **Payload:**
     ::

       {
         "rating": 4,
         "comment": "Good, but could be better."
       }
   - **Response:**
     ::

       {
         "message": "Review updated successfully"
       }

3. **Delete Review**
   - **Method:** DELETE
   - **URL:** `/reviews/delete/<int:review_id>`
   - **Description:** Deletes a review by its ID.
   - **Response:**
     ::

       {
         "message": "Review deleted successfully"
       }

4. **Moderate Review**
   - **Method:** POST
   - **URL:** `/reviews/moderate/<int:review_id>`
   - **Description:** Flags or approves a review for moderation.
   - **Payload:**
     ::

       {
         "status": "approved"
       }
   - **Response:**
     ::

       {
         "message": "Review moderation updated"
       }

5. **Get Product Reviews**
   - **Method:** GET
   - **URL:** `/reviews/product/<int:good_id>`
   - **Description:** Retrieves all reviews for a specific product.
   - **Response:**
     ::

       [
         {
           "customer_username": "johndoe",
           "rating": 5,
           "comment": "Great product!",
           "status": "approved"
         }
       ]

6. **Get Customer Reviews**
   - **Method:** GET
   - **URL:** `/reviews/customer/<customer_username>`
   - **Description:** Retrieves all reviews submitted by a specific customer.
   - **Response:**
     ::

       [
         {
           "good_name": "Laptop",
           "rating": 5,
           "comment": "Excellent performance!",
           "status": "approved"
         }
       ]

Review Workflow
----------------
1. Validate the existence of the customer and product before submitting a review.
2. Allow customers to update or delete their own reviews.
3. Enable administrators to approve or flag inappropriate reviews.
4. Maintain review history for transparency and analysis.

Database Schema
----------------
The service interacts with the following tables:

1. **Reviews:**
   - **id (int):** Unique identifier for the review (Primary Key).
   - **customer_username (str):** Username of the customer who submitted the review.
   - **good_id (int):** ID of the reviewed good.
   - **rating (int):** Rating given by the customer (e.g., 1-5).
   - **comment (str):** Feedback provided by the customer.
   - **status (str):** Status of the review (e.g., "approved", "flagged").

---
