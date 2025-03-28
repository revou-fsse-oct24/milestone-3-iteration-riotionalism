from app.models import db, Account
import uuid

class AccountRepository:
    @staticmethod
    def create(account_data):
        account = Account(
            user_id=account_data['user_id'],
            account_type=account_data['account_type'],
            account_number=str(uuid.uuid4())[:8].upper()
        )
        db.session.add(account)
        db.session.commit()
        return account

    @staticmethod
    def get_all():
        return Account.query.all()

    @staticmethod
    def get_by_id(account_id):
        return Account.query.get(account_id)

    @staticmethod
    def get_by_user(user_id):
        return Account.query.filter_by(user_id=user_id).all()

    @staticmethod
    def update(account_id, account_data):
        account = Account.query.get(account_id)
        if account:
            account.account_type = account_data.get('account_type', account.account_type)
            db.session.commit()
        return account

    @staticmethod
    def delete(account_id):
        account = Account.query.get(account_id)
        if account:
            db.session.delete(account)
            db.session.commit()
            return True
        return False
