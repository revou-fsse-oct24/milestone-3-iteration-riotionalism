from datetime import datetime
from app.models import db, Transaction, Account
from sqlalchemy import or_

class TransactionRepository:
    def __init__(self):
        self.transactions = {}
        self.current_id = 1

    @staticmethod
    def create(transaction_data):
        transaction = Transaction(
            from_account_id=transaction_data.get('from_account'),
            to_account_id=transaction_data.get('to_account'),
            amount=transaction_data['amount'],
            type=transaction_data['type'],
            description=transaction_data.get('description', '')
        )
        
        # Update account balances
        if transaction.type == 'deposit':
            to_account = Account.query.get(transaction.to_account_id)
            to_account.balance += transaction.amount
        elif transaction.type == 'withdrawal':
            from_account = Account.query.get(transaction.from_account_id)
            from_account.balance -= transaction.amount
        elif transaction.type == 'transfer':
            from_account = Account.query.get(transaction.from_account_id)
            to_account = Account.query.get(transaction.to_account_id)
            from_account.balance -= transaction.amount
            to_account.balance += transaction.amount

        db.session.add(transaction)
        db.session.commit()
        return transaction

    @staticmethod
    def get_all(account_id=None):
        if account_id:
            return Transaction.query.filter(
                or_(
                    Transaction.from_account_id == account_id,
                    Transaction.to_account_id == account_id
                )
            ).all()
        return Transaction.query.all()

    @staticmethod
    def get_by_id(transaction_id):
        return Transaction.query.get(transaction_id)
