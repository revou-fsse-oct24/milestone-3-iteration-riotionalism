from flask import jsonify, request
from app.repositories.account_repository import AccountRepository

account_repository = AccountRepository()

class AccountView:
    @staticmethod
    def get_all_accounts():
        accounts = account_repository.get_all()
        return jsonify(accounts), 200

    @staticmethod
    def get_account(account_id):
        account = account_repository.get_by_id(account_id)
        if account:
            return jsonify(account), 200
        return jsonify({"error": "Account not found"}), 404

    @staticmethod
    def create_account():
        try:
            data = request.get_json()
            required_fields = ['account_type', 'user_id']
            
            if not all(field in data for field in required_fields):
                return jsonify({"error": "Missing required fields"}), 400
                
            account = account_repository.create(data)
            return jsonify({
                "message": "Account created successfully",
                "data": account
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
