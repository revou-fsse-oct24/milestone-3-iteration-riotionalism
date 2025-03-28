from app import db
from app.models import Account
import random
import string

class AccountRepository:
    def generate_account_number(self):
        # Generate random 10-digit account number
        return ''.join(random.choices(string.digits, k=10))

    def create_account(self, user_id, account_type):
        try:
            # Validasi account_type
            valid_types = ['savings', 'checking']
            if account_type not in valid_types:
                raise ValueError("Invalid account type")

            # Cek nomor akun unik
            account_number = self.generate_account_number()
            while self.get_account_by_number(account_number):
                account_number = self.generate_account_number()

            account = Account(
                user_id=user_id,
                account_type=account_type,
                account_number=account_number,
                balance=0.0
            )
            db.session.add(account)
            db.session.commit()
            return account
        except Exception as e:
            db.session.rollback()
            raise e

    def get_account_by_id(self, account_id):
        return Account.query.get(account_id)

    def get_user_accounts(self, user_id):
        return Account.query.filter_by(user_id=user_id).all()

    def get_account_by_number(self, account_number):
        return Account.query.filter_by(account_number=account_number).first()

    def update_balance(self, account_id, new_balance):
        try:
            account = self.get_account_by_id(account_id)
            if not account:
                raise ValueError("Account not found")
            if new_balance < 0:
                raise ValueError("Balance cannot be negative")
            
            account.balance = new_balance
            db.session.commit()
            return account
        except Exception as e:
            db.session.rollback()
            raise e
