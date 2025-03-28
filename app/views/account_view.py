from flask import jsonify, request
from flask_login import current_user, login_required
from app.repositories.account_repository import AccountRepository

class AccountView:
    @staticmethod
    @login_required
    def create_account():
        try:
            data = request.get_json()
            data['user_id'] = current_user.id
            
            if 'account_type' not in data:
                return jsonify({"error": "Account type is required"}), 400
                
            account = AccountRepository.create(data)
            return jsonify({
                "message": "Account created successfully",
                "data": {
                    "id": account.id,
                    "account_type": account.account_type,
                    "account_number": account.account_number,
                    "balance": float(account.balance)
                }
            }), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    @login_required
    def get_all_accounts():
        accounts = AccountRepository.get_by_user(current_user.id)
        return jsonify([{
            "id": acc.id,
            "account_type": acc.account_type,
            "account_number": acc.account_number,
            "balance": float(acc.balance)
        } for acc in accounts]), 200

    @staticmethod
    @login_required
    def get_account(account_id):
        account = AccountRepository.get_by_id(account_id)
        if account and account.user_id == current_user.id:
            return jsonify({
                "id": account.id,
                "account_type": account.account_type,
                "account_number": account.account_number,
                "balance": float(account.balance)
            }), 200
        return jsonify({"error": "Account not found"}), 404

    @staticmethod
    @login_required
    def update_account(account_id):
        try:
            account = AccountRepository.get_by_id(account_id)
            if not account or account.user_id != current_user.id:
                return jsonify({"error": "Account not found"}), 404

            data = request.get_json()
            updated_account = AccountRepository.update(account_id, data)
            return jsonify({
                "message": "Account updated successfully",
                "data": {
                    "id": updated_account.id,
                    "account_type": updated_account.account_type,
                    "account_number": updated_account.account_number,
                    "balance": float(updated_account.balance)
                }
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    @login_required
    def delete_account(account_id):
        account = AccountRepository.get_by_id(account_id)
        if not account or account.user_id != current_user.id:
            return jsonify({"error": "Account not found"}), 404

        if AccountRepository.delete(account_id):
            return jsonify({"message": "Account deleted successfully"}), 200
        return jsonify({"error": "Failed to delete account"}), 400
