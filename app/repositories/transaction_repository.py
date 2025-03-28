from app import db
from app.models import Transaction, Account
from decimal import Decimal

class TransactionRepository:
    def create_transaction(self, from_account_id, to_account_id, amount, type, description=""):
        try:
            # Validasi tipe transaksi
            valid_types = ['deposit', 'withdrawal', 'transfer']
            if type not in valid_types:
                raise ValueError("Invalid transaction type")

            # Validasi jumlah
            if amount <= 0:
                raise ValueError("Amount must be positive")

            transaction = Transaction(
                from_account_id=from_account_id,
                to_account_id=to_account_id,
                amount=amount,
                type=type,
                description=description,
                status='completed'  # Tambahkan status
            )
            db.session.add(transaction)
            db.session.commit()
            return transaction
        except Exception as e:
            db.session.rollback()
            raise e

    def get_transaction_by_id(self, transaction_id):
        return Transaction.query.get(transaction_id)

    def get_account_transactions(self, account_id):
        return Transaction.query.filter(
            (Transaction.from_account_id == account_id) |
            (Transaction.to_account_id == account_id)
        ).all()

    def process_transfer(self, from_account_id, to_account_id, amount, description=""):
        try:
            from_account = Account.query.get(from_account_id)
            to_account = Account.query.get(to_account_id)
            
            if not from_account or not to_account:
                raise ValueError("Account not found")
            
            if from_account.balance < Decimal(str(amount)):
                raise ValueError("Insufficient funds")

            # Update balances
            from_account.balance -= Decimal(str(amount))
            to_account.balance += Decimal(str(amount))

            # Create transaction record
            transaction = self.create_transaction(
                from_account_id=from_account_id,
                to_account_id=to_account_id,
                amount=amount,
                type="transfer",
                description=description
            )

            db.session.commit()
            return transaction
        except Exception as e:
            db.session.rollback()
            raise e

    # Method baru untuk deposit
    def process_deposit(self, to_account_id, amount, description=""):
        try:
            to_account = Account.query.get(to_account_id)
            if not to_account:
                raise ValueError("Account not found")

            to_account.balance += Decimal(str(amount))
            
            transaction = self.create_transaction(
                from_account_id=None,
                to_account_id=to_account_id,
                amount=amount,
                type="deposit",
                description=description
            )

            db.session.commit()
            return transaction
        except Exception as e:
            db.session.rollback()
            raise e

    # Method baru untuk withdrawal
    def process_withdrawal(self, from_account_id, amount, description=""):
        try:
            from_account = Account.query.get(from_account_id)
            if not from_account:
                raise ValueError("Account not found")
            
            if from_account.balance < Decimal(str(amount)):
                raise ValueError("Insufficient funds")

            from_account.balance -= Decimal(str(amount))
            
            transaction = self.create_transaction(
                from_account_id=from_account_id,
                to_account_id=None,
                amount=amount,
                type="withdrawal",
                description=description
            )

            db.session.commit()
            return transaction
        except Exception as e:
            db.session.rollback()
            raise e
