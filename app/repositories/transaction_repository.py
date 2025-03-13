from datetime import datetime

class TransactionRepository:
    def __init__(self):
        self.transactions = {}
        self.current_id = 1

    def create(self, transaction_data):
        transaction_id = self.current_id
        transaction_data['id'] = transaction_id
        transaction_data['timestamp'] = datetime.now().isoformat()
        transaction_data['status'] = 'completed'  # simplified
        self.transactions[transaction_id] = transaction_data
        self.current_id += 1
        return transaction_data

    def get_all(self, account_id=None):
        transactions = list(self.transactions.values())
        if account_id:
            transactions = [t for t in transactions if t['from_account'] == account_id or t['to_account'] == account_id]
        return transactions

    def get_by_id(self, transaction_id):
        return self.transactions.get(transaction_id)
