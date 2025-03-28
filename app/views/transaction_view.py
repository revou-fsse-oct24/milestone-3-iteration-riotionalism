from flask import jsonify, request
from flask_login import current_user, login_required
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.account_repository import AccountRepository

class TransactionView:
    @staticmethod
    @login_required
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
            try:
                amount = float(data['amount'])
                if amount <= 0:
                    return jsonify({"error": "Amount must be positive"}), 400
            except ValueError:
                return jsonify({"error": "Invalid amount"}), 400

            # Validate accounts and ownership
            if data['type'] in ['withdrawal', 'transfer']:
                from_account = AccountRepository.get_by_id(data['from_account'])
                if not from_account or from_account.user_id != current_user.id:
                    return jsonify({"error": "Invalid source account"}), 400
                if float(from_account.balance) < amount:
                    return jsonify({"error": "Insufficient funds"}), 400

            if data['type'] in ['deposit', 'transfer']:
                to_account = AccountRepository.get_by_id(data['to_account'])
                if not to_account:
                    return jsonify({"error": "Invalid destination account"}), 400

            transaction = TransactionRepository.create(data)
            return jsonify({
                "message": "Transaction completed successfully",
                "data": {
                    "id": transaction.id,
                    "type": transaction.type,
                    "amount": float(transaction.amount),
                    "created_at": transaction.created_at.isoformat()
                }
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    @login_required
    def get_all_transactions():
        account_id = request.args.get('account_id', type=int)
        if account_id:
            account = AccountRepository.get_by_id(account_id)
            if not account or account.user_id != current_user.id:
                return jsonify({"error": "Invalid account"}), 400

        transactions = TransactionRepository.get_all(account_id)
        return jsonify([{
            "id": t.id,
            "type": t.type,
            "amount": float(t.amount),
            "from_account": t.from_account_id,
            "to_account": t.to_account_id,
            "description": t.description,
            "created_at": t.created_at.isoformat()
        } for t in transactions]), 200

    @staticmethod
    @login_required
    def get_transaction(transaction_id):
        transaction = TransactionRepository.get_by_id(transaction_id)
        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404

        # Verify user has access to this transaction
        if transaction.from_account and transaction.from_account.user_id != current_user.id:
            if transaction.to_account and transaction.to_account.user_id != current_user.id:
                return jsonify({"error": "Transaction not found"}), 404

        return jsonify({
            "id": transaction.id,
            "type": transaction.type,
            "amount": float(transaction.amount),
            "from_account": transaction.from_account_id,
            "to_account": transaction.to_account_id,
            "description": transaction.description,
            "created_at": transaction.created_at.isoformat()
        }), 200
