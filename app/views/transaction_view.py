from flask import jsonify, request
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.account_repository import AccountRepository

transaction_repository = TransactionRepository()
account_repository = AccountRepository()

class TransactionView:
    @staticmethod
    def get_all_transactions():
        account_id = request.args.get('account_id', type=int)
        transactions = transaction_repository.get_all(account_id)
        return jsonify(transactions), 200

    @staticmethod
    def get_transaction(transaction_id):
        transaction = transaction_repository.get_by_id(transaction_id)
        if transaction:
            return jsonify(transaction), 200
        return jsonify({"error": "Transaction not found"}), 404

    @staticmethod
    def create_transaction():
        try:
            data = request.get_json()
            required_fields = ['type', 'amount']
            
            if not all(field in data for field in required_fields):
                return jsonify({"error": "Missing required fields"}), 400

            # Validate transaction type
            valid_types = ['deposit', 'withdrawal', 'transfer']
            if data['type'] not in valid_types:
                return jsonify({"error": "Invalid transaction type"}), 400

            # Validate amount
            if not isinstance(data['amount'], (int, float)) or data['amount'] <= 0:
                return jsonify({"error": "Invalid amount"}), 400

            # Additional validation for transfer
            if data['type'] == 'transfer':
                if not all(field in data for field in ['from_account', 'to_account']):
                    return jsonify({"error": "Transfer requires from_account and to_account"}), 400

            transaction = transaction_repository.create(data)
            return jsonify({
                "message": "Transaction created successfully",
                "data": transaction
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400
