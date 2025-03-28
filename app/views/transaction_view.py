from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from decimal import Decimal
from app.repositories import TransactionRepository, AccountRepository

transaction_repository = TransactionRepository()
account_repository = AccountRepository()

class TransactionView:
    @staticmethod
    @jwt_required()
    def get_account_transactions(account_number):
        try:
            current_user_id = get_jwt_identity()
            account = account_repository.get_account_by_number(account_number)
            
            if not account:
                return jsonify({"error": "Account not found"}), 404
                
            if account.user_id != current_user_id:
                return jsonify({"error": "Unauthorized"}), 403
                
            transactions = transaction_repository.get_account_transactions(account.id)
            
            return jsonify([{
                'id': tx.id,
                'type': tx.type,
                'amount': float(tx.amount),
                'description': tx.description,
                'created_at': tx.created_at.isoformat(),
                'status': tx.status
            } for tx in transactions]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    @jwt_required()
    def create_deposit():
        try:
            current_user_id = get_jwt_identity()
            data = request.get_json()
            
            if not all(k in data for k in ['account_number', 'amount']):
                return jsonify({"error": "Missing required fields"}), 400
                
            account = account_repository.get_account_by_number(data['account_number'])
            
            if not account:
                return jsonify({"error": "Account not found"}), 404
                
            if account.user_id != current_user_id:
                return jsonify({"error": "Unauthorized"}), 403
                
            amount = Decimal(str(data['amount']))
            if amount <= 0:
                return jsonify({"error": "Amount must be positive"}), 400
                
            transaction = transaction_repository.process_deposit(
                to_account_id=account.id,
                amount=amount,
                description=data.get('description', 'Deposit')
            )
            
            return jsonify({
                "message": "Deposit successful",
                "transaction": {
                    'id': transaction.id,
                    'type': transaction.type,
                    'amount': float(transaction.amount),
                    'description': transaction.description,
                    'created_at': transaction.created_at.isoformat(),
                    'status': transaction.status
                }
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400
