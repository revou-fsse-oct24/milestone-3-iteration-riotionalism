# 🏦 RevoBank API

📊 Overview of the API
<div style="text-align: justify">
RevoBank API is a RESTful API built with Flask that implements core banking features for User Management, Account Management, and Transaction Management. This API serves as the backend for the RevoBank application.
</div>

## ✨ Features Implemented
1. 👤 User Management
   <div style="text-align: justify">
   - Create new user account
   - Retrieve user profile
   - Update user profile
   - User authentication (login/register)
   </div>

2. 💳 Account Management
   <div style="text-align: justify">
   - Create new bank account
   - Retrieve account details
   - Update account information
   - List all accounts
   - Delete account
   </div>

3. 💸 Transaction Management
   <div style="text-align: justify">
   - Create transactions (deposit, withdrawal, transfer)
   - Retrieve transaction details
   - List all transactions
   - Filter transactions by account
   </div>

## 📑 Database Schema
FLASK_APP=app
FLASK_ENV=development
DATABASE_URL=sqlite:///revobank.db
JWT_SECRET_KEY=your-super-secret-key-change-this

### 👤 Users Table
- `id` (Integer, Primary Key)
- `username` (String, Unique)
- `email` (String, Unique)
- `password` (String, Hashed)
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

### 💳 Accounts Table
- `id` (Integer, Primary Key)
- `user_id` (Integer, Foreign Key → Users)
- `account_number` (String, Unique)
- `balance` (Float)
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

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

4. Setup environment variables (.env)

5. Run the application
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## 🚀 Deployment
This deployed on Koyeb and can be accessed at: https://wee-bill-riotionalism-e9187ffa.koyeb.app/

## 📝 API Usage Documentation

| 🔗 Documentation Link | Description |
|---------------------|-------------|
| [📚 Click Here to View API Documentation](https://www.apidog.com/apidoc/shared-61623065-9612-491e-afc9-59a12a557d0e) | Complete API documentation with examples and testing playground |

## 🔧 Technologies Used
- Flask (Python Web Framework)
- SQLAlchemy (ORM)
- Flask-JWT-Extended (Authentication)
- PostgreSQL (Production Database)
- SQLite (Development Database)

> 🌟 **Quick Access**: Click the documentation link above to explore our interactive API documentation powered by APIDOG

❤️ TENGKYU, THAT'S ALL!. I LOVE U!