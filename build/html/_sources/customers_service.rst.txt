Customers Service
=================

The Customers Service is responsible for managing customer-related operations in the eCommerce system. This includes registering new customers, updating customer information, managing wallet balances, and retrieving customer details.

Key Responsibilities
---------------------
- **Register Customer:** Add a new customer to the system with all relevant details.
- **Update Customer:** Modify one or more fields of an existing customer's information.
- **Delete Customer:** Remove a customer from the system by username.
- **Retrieve Customers:** Fetch details of all customers or a specific customer by username.
- **Wallet Management:** Add funds to or deduct funds from a customer's wallet.

Available Endpoints
--------------------

1. **Register Customer**
   - **Method:** POST
   - **URL:** `/customers/register`
   - **Description:** Registers a new customer in the system.
   - **Payload:**
     ::

       {
         "full_name": "John Doe",
         "username": "johndoe",
         "password": "password123",
         "age": 30,
         "address": "123 Elm Street",
         "gender": "Male",
         "marital_status": "Single"
       }
   - **Response:** Returns a success message or an error if the username already exists.

2. **Update Customer**
   - **Method:** PUT
   - **URL:** `/customers/update/<username>`
   - **Description:** Updates one or more fields of a customer's information.
   - **Payload:**
     ::

       {
         "field_to_update": "value"
       }
   - **Response:** Returns the updated customer details or an error if the customer is not found.

3. **Delete Customer**
   - **Method:** DELETE
   - **URL:** `/customers/delete/<username>`
   - **Description:** Deletes a customer by username.
   - **Response:** Returns a success message or an error if the customer is not found.

4. **Get All Customers**
   - **Method:** GET
   - **URL:** `/customers/all`
   - **Description:** Retrieves a list of all customers.
   - **Response:** Returns an array of customer details.

5. **Get Customer by Username**
   - **Method:** GET
   - **URL:** `/customers/<username>`
   - **Description:** Retrieves a specific customer's details by username.
   - **Response:** Returns the customer's details or an error if the customer is not found.

6. **Charge Wallet**
   - **Method:** POST
   - **URL:** `/customers/charge/<username>`
   - **Description:** Adds funds to a customer's wallet.
   - **Payload:**
     ::

       {
         "amount": 50.0
       }
   - **Response:** Returns the updated wallet balance or an error if the customer is not found.

7. **Deduct Wallet Balance**
   - **Method:** POST
   - **URL:** `/customers/deduct/<username>`
   - **Description:** Deducts funds from a customer's wallet.
   - **Payload:**
     ::

       {
         "amount": 30.0
       }
   - **Response:** Returns the updated wallet balance or an error if the customer is not found.

Database Schema
----------------
The service uses a single table to store customer data with the following structure:

- **id (int):** Unique identifier for the customer (Primary Key).
- **full_name (str):** Customer's full name.
- **username (str):** Unique username for login.
- **password (str):** Hashed password.
- **age (int):** Customer's age.
- **address (str):** Customer's address.
- **gender (str):** Gender (e.g., Male, Female).
- **marital_status (str):** Marital status (e.g., Single, Married).
- **wallet_balance (float):** Current wallet balance.

---
