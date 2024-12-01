Inventory Service
=================

The Inventory Service is responsible for managing goods in the eCommerce system. This includes adding new goods, updating existing goods, removing goods from stock, and retrieving details about available goods.

Key Responsibilities
---------------------
- **Add Goods:** Add new items to the inventory with their relevant details.
- **Update Goods:** Modify the details of existing items.
- **Deduct Stock:** Reduce the stock count for specific items.
- **Retrieve Goods:** Fetch details of all goods or a specific good by its ID.

Available Endpoints
--------------------

1. **Add Goods**
   - **Method:** POST
   - **URL:** `/inventory/add`
   - **Description:** Adds a new item to the inventory.
   - **Payload:**
     ::

       {
         "name": "Laptop",
         "category": "electronics",
         "price": 900.0,
         "description": "High-performance laptop",
         "stock_count": 20
       }
   - **Response:** Returns a success message and details of the newly added good.

2. **Update Goods**
   - **Method:** PUT
   - **URL:** `/inventory/update/<int:goods_id>`
   - **Description:** Updates the details of an existing good by its ID.
   - **Payload:**
     ::

       {
         "price": 850.0,
         "stock_count": 15
       }
   - **Response:** Returns the updated good details or an error if the good is not found.

3. **Deduct Goods**
   - **Method:** POST
   - **URL:** `/inventory/deduct/<int:goods_id>`
   - **Description:** Deducts a specific quantity from the stock of a good.
   - **Payload:**
     ::

       {
         "quantity": 5
       }
   - **Response:** Returns the updated stock details or an error if the good is not found or if the stock is insufficient.

4. **Get All Goods**
   - **Method:** GET
   - **URL:** `/inventory/all`
   - **Description:** Retrieves a list of all goods in the inventory.
   - **Response:** Returns an array of goods, each with its details.

5. **Get Good by ID**
   - **Method:** GET
   - **URL:** `/inventory/<int:goods_id>`
   - **Description:** Retrieves details of a specific good by its ID.
   - **Response:** Returns the good's details or an error if the good is not found.

Database Schema
----------------
The service uses a single table to store inventory data with the following structure:

- **id (int):** Unique identifier for the good (Primary Key).
- **name (str):** Name of the good.
- **category (str):** Category of the good (e.g., electronics, food, clothing).
- **price (float):** Price per item.
- **description (str):** Description of the good.
- **stock_count (int):** Current stock count of the good.

---

