# WALLET APPLICATION BACKEND

## Introduction
The **Wallet Application Backend** is a FastAPI-based backend application for managing wallet-related functionalities such as transactions, authentication, and rate-limiting. This project utilizes SQLite for database storage and provides secure API routes for interacting with wallet data. Middleware for authentication and rate-limiting ensures robust protection and optimal resource usage.

---

## Routes Explanation

### **Users Routes**
Base Path: `/users`

| HTTP Method | Endpoint         | Description                                   |
|-------------|------------------|-----------------------------------------------|
| `POST`      | `/`              | Create a new user.                           |
| `GET`       | `/{user_id}`     | Retrieve details of a specific user by ID.   |
| `PUT`       | `/{user_id}`     | Update details of a specific user by ID.     |
| `GET`       | `/`              | Retrieve a list of all users.                |

---

### **Wallet Routes**
Base Path: `/wallets`

| HTTP Method | Endpoint                     | Description                                   |
|-------------|------------------------------|-----------------------------------------------|
| `POST`      | `/`                          | Create a new wallet.                          |
| `POST`      | `/{wallet_id}/transactions`  | Create a transaction using wallet ID.         |
| `GET`       | `/{wallet_id}/balance`       | Get the wallet balance using wallet ID.       |
| `GET`       | `/{wallet_id}/transactions`  | Retrieve a list of all transactions of a wallet. |

---

### **Tokens Routes**
Base Path: `/token`

| HTTP Method | Endpoint                     | Description                                   |
|-------------|------------------------------|-----------------------------------------------|
| `GET`       | `/new-token`                 | Get actual token for using .                |
| `GET`       | `/new-test-token`            | Get actual token for testing using pytest.  |

---

## Middleware

### **Authentication Middleware**
- **Purpose**: Validates JWT tokens for protected routes.
- **How it Works**:
  - Extracts the `Authorization` header.
  - Decodes and validates the token.
  - If invalid, responds with a `401 Unauthorized` error.

### **Rate-Limiting Middleware**
- **Purpose**: Restricts requests to prevent abuse (DDoS, brute force).
- **Policy**:
  - General rate limit: **10 calls per minute** per client IP.
  - Returns `429 Too Many Requests` if the limit is exceeded.

---

## Database (SQLite)

### **Tables and Relationships**

#### **Users**
- **Columns**:
  - `id` (Primary Key)
  - `username` (Unique, String)
  - `password_hash` (String)

#### **Transactions**
- **Columns**:
  - `id` (Primary Key)
  - `user_id` (Foreign Key referencing `Users.id`)
  - `transaction_type` (String: "credit" or "debit")
  - `amount` (Float)
  - `timestamp` (DateTime)

#### **Relationships**
- A `User` can have multiple `Transactions`.
- Each `Transaction` belongs to a single `User`.

---

## Getting Started

### **Requirements**
- Python 3.8+
- SQLite
- pip

### **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/Bilal2001/WALLET_APPLICATION_BACKEND.git
   cd WALLET_APPLICATION_BACKEND
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   alembic upgrade head
   ```
5. Create a .env file in the root dir:
   ```bash
   echo -e 'SECRET_KEY="YOUR_VERY_SECRET_KEY"\nALGORITHM="HS256"\n\nRATELIMIT_PER_MINUTE=10' > .env
   ```
7. Start the application:
   ```bash
   uvicorn main:app --reload
   ```

---

## Running Tests

Unit tests are written using `pytest`.

### **Run Tests**
1. Install testing dependencies:
   ```bash
   pip install pytest
   ```
2. Run the tests:
   ```bash
   pytest
   ```

---
