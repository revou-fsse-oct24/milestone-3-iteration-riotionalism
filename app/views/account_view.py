from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.repositories.account_repository import AccountRepository

account_repository = AccountRepository()

class AccountView:
    @staticmethod
    @jwt_required()
    def get_all_accounts():
        current_user_id = get_jwt_identity()
        accounts = account_repository.get_user_accounts(current_user_id)
        return jsonify([{
            'id': acc.id,
            'account_number': acc.account_number,
            'account_type': acc.account_type,
            'balance': float(acc.balance),
            'created_at': acc.created_at.isoformat()
        } for acc in accounts]), 200

    @staticmethod
    @jwt_required()
    def get_account(account_id):
        current_user_id = get_jwt_identity()
        account = account_repository.get_account_by_id(account_id)
        
        if not account:
            return jsonify({"error": "Account not found"}), 404
            
        if account.user_id != current_user_id:
            return jsonify({"error": "Unauthorized"}), 403
            
        return jsonify({
            'id': account.id,
            'account_number': account.account_number,
            'account_type': account.account_type,
            'balance': float(account.balance),
            'created_at': account.created_at.isoformat()
        }), 200

    @staticmethod
    @jwt_required()
    def create_account():
        try:
            current_user_id = get_jwt_identity()
            data = request.get_json()
            
            if 'account_type' not in data:
                return jsonify({"error": "Account type is required"}), 400
                
            if data['account_type'] not in ['savings', 'checking']:
                return jsonify({"error": "Invalid account type"}), 400
                
            account = account_repository.create_account(
                user_id=current_user_id,
                account_type=data['account_type']
            )
            
            return jsonify({
                "message": "Account created successfully",
                "account": {
                    'id': account.id,
                    'account_number': account.account_number,
                    'account_type': account.account_type,
                    'balance': float(account.balance),
                    'created_at': account.created_at.isoformat()
                }
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def update_account(account_id):
        try:
            data = request.get_json()
            account = account_repository.update(account_id, data)
            if account:
                return jsonify({
                    "message": "Account updated successfully",
                    "data": account
                }), 200
            return jsonify({"error": "Account not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    def delete_account(account_id):
        if account_repository.delete(account_id):
            return jsonify({"message": "Account deleted successfully"}), 200
        return jsonify({"error": "Account not found"}), 404
