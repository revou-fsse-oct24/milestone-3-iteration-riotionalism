from flask import Blueprint
from app.views.transaction_view import TransactionView

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/transactions', methods=['GET'])
def get_all_transactions():
    return TransactionView.get_all_transactions()

@transaction_bp.route('/transactions/<int:transaction_id>', methods=['GET'])
def get_transaction(transaction_id):
    return TransactionView.get_transaction(transaction_id)

@transaction_bp.route('/transactions', methods=['POST'])
def create_transaction():
    return TransactionView.create_transaction()
