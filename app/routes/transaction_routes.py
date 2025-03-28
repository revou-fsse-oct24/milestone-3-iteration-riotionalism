from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.repositories import TransactionRepository, AccountRepository
from decimal import Decimal

transaction_bp = Blueprint('transaction', __name__)
transaction_repo = TransactionRepository()
account_repo = AccountRepository()

@transaction_bp.route('/transactions/transfer', methods=['POST'])
@jwt_required()
def transfer():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not all(k in data for k in ['from_account_number', 'to_account_number', 'amount']):
            return jsonify({'error': 'Missing required fields'}), 400
            
        # Validasi akun
        from_account = account_repo.get_account_by_number(data['from_account_number'])
        to_account = account_repo.get_account_by_number(data['to_account_number'])
        
        if not from_account or not to_account:
            return jsonify({'error': 'Invalid account number'}), 400
            
        if from_account.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
            
        # Proses transfer
        transaction = transaction_repo.process_transfer(
            from_account_id=from_account.id,
            to_account_id=to_account.id,
            amount=Decimal(str(data['amount'])),
            description=data.get('description', '')
        )
        
        return jsonify({
            'message': 'Transfer successful',
            'transaction': {
                'id': transaction.id,
                'amount': float(transaction.amount),
                'type': transaction.type,
                'description': transaction.description,
                'created_at': transaction.created_at.isoformat()
            }
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@transaction_bp.route('/transactions/deposit', methods=['POST'])
@jwt_required()
def deposit():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not all(k in data for k in ['account_number', 'amount']):
            return jsonify({'error': 'Missing required fields'}), 400
            
        account = account_repo.get_account_by_number(data['account_number'])
        
        if not account:
            return jsonify({'error': 'Invalid account number'}), 400
            
        if account.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
            
        transaction = transaction_repo.process_deposit(
            to_account_id=account.id,
            amount=Decimal(str(data['amount'])),
            description=data.get('description', 'Deposit')
        )
        
        return jsonify({
            'message': 'Deposit successful',
            'transaction': {
                'id': transaction.id,
                'amount': float(transaction.amount),
                'type': transaction.type,
                'description': transaction.description,
                'created_at': transaction.created_at.isoformat()
            }
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@transaction_bp.route('/transactions/withdraw', methods=['POST'])
@jwt_required()
def withdraw():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not all(k in data for k in ['account_number', 'amount']):
            return jsonify({'error': 'Missing required fields'}), 400
            
        account = account_repo.get_account_by_number(data['account_number'])
        
        if not account:
            return jsonify({'error': 'Invalid account number'}), 400
            
        if account.user_id != current_user_id:
            return jsonify({'error': 'Unauthorized'}), 403
            
        transaction = transaction_repo.process_withdrawal(
            from_account_id=account.id,
            amount=Decimal(str(data['amount'])),
            description=data.get('description', 'Withdrawal')
        )
        
        return jsonify({
            'message': 'Withdrawal successful',
            'transaction': {
                'id': transaction.id,
                'amount': float(transaction.amount),
                'type': transaction.type,
                'description': transaction.description,
                'created_at': transaction.created_at.isoformat()
            }
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
