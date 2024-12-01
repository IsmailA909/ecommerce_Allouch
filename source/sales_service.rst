Sales Service
=============

The Sales Service manages customer purchases and displays available goods. It facilitates the purchase process by ensuring sufficient stock and wallet balance and updates inventory and customer wallet upon successful transactions.

Key Responsibilities
---------------------
- **Display Goods:** Show all available goods with basic details.
- **Get Good Details:** Retrieve detailed information about a specific good.
- **Make a Purchase:** Process a customer's purchase of a good, validate stock and balance, and update records.
- **Purchase History:** Retrieve the history of purchases for a specific customer.

Available Endpoints
--------------------

1. **Display Goods**
   - **Method:** GET
   - **URL:** `/sales/goods`
   - **Description:** Retrieves a list of available goods with their names and prices.
   - **Response:**
     ::

       [
         {
           "name": "Laptop",
           "price": 900.0
         },
         {
           "name": "Phone",
           "price": 500.0
         }
       ]

2. **Get Good Details**
   - **Method:** GET
   - **URL:** `/sales/goods/<int:good_id>`
   - **Description:** Retrieves detailed information about a specific good by its ID.
   - **Response:**
     ::

       {
         "name": "Laptop",
         "category": "electronics",
         "price": 900.0,
         "description": "High-performance laptop",
         "stock_count": 20
       }

3. **Make a Purchase**
   - **Method:** POST
   - **URL:** `/sales/purchase`
   - **Description:** Processes a purchase request for a customer.
   - **Payload:**
     ::

       {
         "customer_username": "johndoe",
         "good_id": 1,
         "quantity": 2
       }
   - **Response:** Returns a success message with the purchase details, or an error if conditions are not met (e.g., insufficient stock or wallet balance).

4. **Purchase History**
   - **Method:** GET
   - **URL:** `/sales/history/<customer_username>`
   - **Description:** Retrieves all past purchases for a specific customer.
   - **Response:**
     ::

       [
         {
           "good_name": "Laptop",
           "quantity": 1,
           "total_price": 900.0
         },
         {
           "good_name": "Phone",
           "quantity": 2,
           "total_price": 1000.0
         }
       ]

Purchase Workflow
-----------------
1. Validate the existence of the customer and the good.
2. Ensure the customer's wallet balance is sufficient for the purchase.
3. Deduct the required stock from the inventory.
4. Deduct the total price from the customer's wallet.
5. Record the purchase details for history.

Database Schema
----------------
The service interacts with the following tables:

1. **Purchases:**
   - **id (int):** Unique identifier for the purchase (Primary Key).
   - **customer_username (str):** Username of the customer who made the purchase.
   - **good_id (int):** ID of the purchased good.
   - **quantity (int):** Quantity of the good purchased.
   - **total_price (float):** Total price of the purchase.

---

