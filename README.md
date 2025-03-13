# 🏦 RevoBank API

📊 Overview of the API
RevoBank API is a RESTful API built with Flask that implements core banking features for User Management, Account Management, and Transaction Management. This API serves as the backend for the RevoBank application.

## ✨ Features Implemented
1. 👤 User Management
   - Create new user account
   - Retrieve user profile
   - Update user profile

2. 💳 Account Management
   - Create new bank account
   - Retrieve account details
   - Update account information
   - List all accounts
   - Delete account

3. 💸 Transaction Management
   - Create transactions (deposit, withdrawal, transfer)
   - Retrieve transaction details
   - List all transactions
   - Filter transactions by account

## 🛠️ Installation and Setup Instructions
1. Clone the repository
```bash
git clone [repository-url]
cd revobank-api
```

2. Create and activate virtual environment
```bash
uv venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies
```bash
uv pip install -r requirements.txt
```

4. Run the application
```bash
python main.py
```

The API will be available at `http://localhost:5000`

## 📝 API Usage Documentation

### 🔍 Request & Response Examples

👤 1. Create User
POST /users
Request:
{
"username": "riotionalism",
"email": "fytrioamando@gmail.com",
"password": "rahasia"
}
Response: 201 Created
{
"message": "User created successfully",
"data": {
"id": 1,
"username": "riotionalism",
"email": "fytrioamando@gmail.com"
}
}

💰 2. Create Account
POST /accounts
Request:
{
"account_type": "savings",
"user_id": 1
}
Response: 201 Created
{
"message": "Account created successfully",
"data": {
"id": 1,
"account_type": "savings",
"user_id": 1
}
}

💱 3. Create Transaction
POST /transactions
Request:
{
"type": "deposit",
"amount": 1000,
"to_account": 1
}
Response: 201 Created
{
"message": "Transaction completed successfully",
"data": {
"id": 1,
"type": "deposit",
"amount": 1000,
"timestamp": "2024-03-14T10:30:00"
}
}

⚠️ Error Response Format
400 Bad Request
{
"error": "Missing required fields"
}
404 Not Found
{
"error": "Resource not found"
}

❤️ TENGKYU, THAT'S ALL!. I LOVE U!