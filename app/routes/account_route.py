from flask import Blueprint
from app.views.account_view import AccountView

account_bp = Blueprint('account', __name__)

@account_bp.route('/accounts', methods=['GET'])
def get_all_accounts():
    return AccountView.get_all_accounts()

@account_bp.route('/accounts/<int:account_id>', methods=['GET'])
def get_account(account_id):
    return AccountView.get_account(account_id)

@account_bp.route('/accounts', methods=['POST'])
def create_account():
    return AccountView.create_account()

@account_bp.route('/accounts/<int:account_id>', methods=['PUT'])
def update_account(account_id):
    return AccountView.update_account(account_id)

@account_bp.route('/accounts/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    return AccountView.delete_account(account_id)
