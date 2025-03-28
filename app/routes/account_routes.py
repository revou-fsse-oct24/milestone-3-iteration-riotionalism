from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.repositories import AccountRepository, UserRepository

account_bp = Blueprint('account', __name__)
account_repo = AccountRepository()
user_repo = UserRepository()

@account_bp.route('/accounts', methods=['POST'])
@jwt_required()
def create_account():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if 'account_type' not in data:
            return jsonify({'error': 'Account type is required'}), 400
            
        account = account_repo.create_account(
            user_id=current_user_id,
            account_type=data['account_type']
        )
        
        return jsonify({
            'message': 'Account created successfully',
            'account': {
                'id': account.id,
                'account_number': account.account_number,
                'account_type': account.account_type,
                'balance': float(account.balance)
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@account_bp.route('/accounts', methods=['GET'])
@jwt_required()
def get_user_accounts():
    try:
        current_user_id = get_jwt_identity()
        accounts = account_repo.get_user_accounts(current_user_id)
        
        return jsonify({
            'accounts': [{
                'id': acc.id,
                'account_number': acc.account_number,
                'account_type': acc.account_type,
                'balance': float(acc.balance)
            } for acc in accounts]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@account_bp.route('/accounts/<account_number>', methods=['GET'])
@jwt_required()
def get_account_detail(account_number):
    try:
        current_user_id = get_jwt_identity()
        account = account_repo.get_account_by_number(account_number)
        
        if not account:
            return jsonify({'error': 'Account not found'}), 404
            
        if account.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
            
        return jsonify({
            'account': {
                'id': account.id,
                'account_number': account.account_number,
                'account_type': account.account_type,
                'balance': float(account.balance),
                'created_at': account.created_at.isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 